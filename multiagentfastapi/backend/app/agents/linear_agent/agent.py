import asyncio
from .client import LinearClient
from .collector import StoryCollector, CollectorState
from app.session import session_manager


class LinearAgent:
    def __init__(self):
        self.client = LinearClient()

    async def run(self, session_id: str, user_message: str, send_event) -> str:
        """
        Handle a turn of the Linear agent conversation.
        Maintains state in session_manager under 'agent_state'.
        """
        session = session_manager.get(session_id)

        # Get or create collector for this session
        collector: StoryCollector = session.get("agent_state")
        if collector is None:
            collector = StoryCollector()
            # Fetch teams upfront
            await send_event({"type": "status", "message": "Fetching your Linear teams..."})
            try:
                teams = await self.client.get_teams()
                collector.teams = teams
            except Exception as e:
                await send_event({"type": "error", "message": f"Could not connect to Linear: {str(e)}"})
                return ""
            session_manager.update(session_id, "agent_state", collector)
            # Return first question without processing user message
            return collector.get_next_question()

        # Process user answer
        next_question = collector.process_answer(user_message)

        if collector.is_done():
            # Create everything in Linear
            return await self._create_in_linear(collector, send_event)

        return next_question or collector.get_next_question()

    async def _create_in_linear(self, collector: StoryCollector, send_event) -> str:
        data = collector.data

        await send_event({"type": "status", "message": f"Creating project '{data.name}' in Linear..."})

        try:
            project = await self.client.create_project(
                name=data.name,
                description=data.description,
                team_id=data.team_id,
            )
        except Exception as e:
            await send_event({"type": "error", "message": f"Failed to create project: {str(e)}"})
            return ""

        await send_event({"type": "status", "message": f"Creating {len(data.stories)} stories..."})

        created = []
        for i, story in enumerate(data.stories, 1):
            await send_event({
                "type": "status",
                "message": f"Creating story {i}/{len(data.stories)}: {story.title}"
            })
            try:
                issue = await self.client.create_issue(
                    title=story.title,
                    description=story.description,
                    team_id=data.team_id,
                    project_id=project["id"],
                    priority=story.priority,
                    estimate=story.estimate,
                )
                created.append(issue)
            except Exception as e:
                await send_event({"type": "error", "message": f"Failed to create story '{story.title}': {str(e)}"})

        project_url = project.get("url", "")
        lines = [
            f"Done! Created project **{data.name}** in Linear with {len(created)} stories.",
            "",
        ]
        for issue in created:
            lines.append(f"- [{issue['title']}]({issue['url']})")
        if project_url:
            lines.append(f"\n[Open project in Linear]({project_url})")

        return "\n".join(lines)
