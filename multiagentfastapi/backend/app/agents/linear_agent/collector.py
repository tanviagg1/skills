from enum import Enum
from dataclasses import dataclass, field


class CollectorState(Enum):
    GATHERING_PROJECT_NAME = "gathering_project_name"
    GATHERING_PROJECT_DESC = "gathering_project_desc"
    GATHERING_TEAM = "gathering_team"
    GATHERING_STORIES = "gathering_stories"
    CONFIRMING = "confirming"
    DONE = "done"


@dataclass
class Story:
    title: str
    description: str = ""
    priority: int = 3  # default: medium
    estimate: int = None


@dataclass
class ProjectData:
    name: str = ""
    description: str = ""
    team_id: str = ""
    team_name: str = ""
    stories: list[Story] = field(default_factory=list)


PRIORITY_MAP = {
    "urgent": 1, "high": 2, "medium": 3, "low": 4,
    "no priority": 0, "none": 0,
}


class StoryCollector:
    def __init__(self):
        self.state = CollectorState.GATHERING_PROJECT_NAME
        self.data = ProjectData()
        self.teams: list[dict] = []
        self._pending_story: dict = {}

    def is_done(self) -> bool:
        return self.state == CollectorState.DONE

    def get_next_question(self) -> str:
        if self.state == CollectorState.GATHERING_PROJECT_NAME:
            return "What's the name of the project?"

        if self.state == CollectorState.GATHERING_PROJECT_DESC:
            return "Give me a short description or goal for this project."

        if self.state == CollectorState.GATHERING_TEAM:
            team_list = "\n".join(
                [f"  {i+1}. {t['name']}" for i, t in enumerate(self.teams)]
            )
            return f"Which team should this project belong to?\n{team_list}"

        if self.state == CollectorState.GATHERING_STORIES:
            if not self.data.stories:
                return "Let's add stories. What's the title of the first story?"
            return "What's the next story title? (or type 'done' if you're finished)"

        if self.state == CollectorState.CONFIRMING:
            return self._confirmation_message()

        return ""

    def process_answer(self, answer: str) -> str | None:
        """
        Process the user's answer for the current state.
        Returns the next question, or None if moving to confirmation.
        """
        answer = answer.strip()

        if self.state == CollectorState.GATHERING_PROJECT_NAME:
            self.data.name = answer
            self.state = CollectorState.GATHERING_PROJECT_DESC
            return self.get_next_question()

        if self.state == CollectorState.GATHERING_PROJECT_DESC:
            self.data.description = answer
            self.state = CollectorState.GATHERING_TEAM
            return self.get_next_question()

        if self.state == CollectorState.GATHERING_TEAM:
            team = self._match_team(answer)
            if not team:
                return f"I didn't recognise that team. Please pick from:\n" + \
                    "\n".join([f"  {i+1}. {t['name']}" for i, t in enumerate(self.teams)])
            self.data.team_id = team["id"]
            self.data.team_name = team["name"]
            self.state = CollectorState.GATHERING_STORIES
            return self.get_next_question()

        if self.state == CollectorState.GATHERING_STORIES:
            if answer.lower() in ("done", "that's all", "thats all", "no more", "finished"):
                if not self.data.stories:
                    return "You need at least one story. What's the first story title?"
                self.state = CollectorState.CONFIRMING
                return self.get_next_question()

            # Check if we're waiting for priority/estimate for a pending story
            if self._pending_story:
                self._parse_story_details(answer)
                return self.get_next_question()

            # New story title
            self._pending_story = {"title": answer}
            return f"Priority and estimate for '{answer}'? (e.g. 'high, 3 points' or just press enter to skip)"

        if self.state == CollectorState.CONFIRMING:
            if answer.lower() in ("yes", "looks good", "confirm", "create", "go ahead", "ok", "okay"):
                self.state = CollectorState.DONE
                return None
            elif answer.lower() in ("no", "edit", "change"):
                # Go back to gathering stories
                self.state = CollectorState.GATHERING_STORIES
                return "What would you like to change? Tell me the story title or type a new story."
            else:
                return "Please confirm with 'yes' to create, or 'edit' to make changes."

        return None

    def _parse_story_details(self, text: str):
        """Parse priority and estimate from a free-text answer."""
        priority = 3  # default medium
        estimate = None

        lower = text.lower()
        for word, val in PRIORITY_MAP.items():
            if word in lower:
                priority = val
                break

        import re
        match = re.search(r"(\d+)\s*(point|pt|sp|story point)?", lower)
        if match:
            estimate = int(match.group(1))

        story = Story(
            title=self._pending_story["title"],
            priority=priority,
            estimate=estimate,
        )
        self.data.stories.append(story)
        self._pending_story = {}

    def _match_team(self, answer: str) -> dict | None:
        lower = answer.lower().strip()
        for team in self.teams:
            if team["name"].lower() == lower:
                return team
        # try by number
        if answer.isdigit():
            idx = int(answer) - 1
            if 0 <= idx < len(self.teams):
                return self.teams[idx]
        # partial match
        for team in self.teams:
            if lower in team["name"].lower():
                return team
        return None

    def _confirmation_message(self) -> str:
        lines = [
            "Here's a summary of what I'll create in Linear:",
            "",
            f"**Project:** {self.data.name}",
            f"**Description:** {self.data.description}",
            f"**Team:** {self.data.team_name}",
            "",
            f"**Stories ({len(self.data.stories)}):**",
        ]
        priority_labels = {0: "None", 1: "Urgent", 2: "High", 3: "Medium", 4: "Low"}
        for i, story in enumerate(self.data.stories, 1):
            est = f", {story.estimate}pts" if story.estimate else ""
            lines.append(
                f"  {i}. {story.title} — {priority_labels.get(story.priority, 'Medium')}{est}"
            )
        lines.append("")
        lines.append("Type **yes** to create, or **edit** to make changes.")
        return "\n".join(lines)
