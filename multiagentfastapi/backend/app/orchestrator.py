import json
from pathlib import Path
from groq import Groq
from app.config import settings
from app.session import session_manager
from app.agents.github_agent.agent import GitHubAgent
from app.agents.linear_agent.agent import LinearAgent

PROMPT_PATH = Path(__file__).parent / "prompts" / "router.md"

ROUTER_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "route_to_github",
            "description": "Route to GitHub agent when user provides a GitHub repo URL or asks to analyse code, understand a repo, or generate a sequence diagram.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "The GitHub repository URL"},
                    "intent": {"type": "string", "description": "What the user wants to do with the repo"},
                },
                "required": ["repo_url", "intent"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "route_to_linear",
            "description": "Route to Linear agent when user wants to create a project, stories, issues, tasks, or tickets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "context": {"type": "string", "description": "Summary of what the user wants to create"},
                },
                "required": ["context"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "respond_directly",
            "description": "Respond directly to the user for greetings, capability questions, or unclear intent.",
            "parameters": {
                "type": "object",
                "properties": {
                    "response": {"type": "string", "description": "The response to send to the user"},
                },
                "required": ["response"],
            },
        },
    },
]


class Orchestrator:
    def __init__(self):
        self.system_prompt = PROMPT_PATH.read_text()
        self.client = Groq(api_key=settings.groq_api_key)
        self.github_agent = GitHubAgent()
        self.linear_agent = LinearAgent()

    async def handle(self, session_id: str, user_message: str, send_event):
        session = session_manager.get(session_id)
        active_agent = session.get("active_agent")

        # If a Linear conversation is already in progress, keep routing there
        if active_agent == "linear":
            response = await self.linear_agent.run(session_id, user_message, send_event)
            agent_state = session_manager.get(session_id).get("agent_state")
            if agent_state and agent_state.is_done():
                session_manager.update(session_id, "active_agent", None)
                session_manager.update(session_id, "agent_state", None)
            return response

        session_manager.append_message(session_id, "user", user_message)
        history = session_manager.get(session_id)["history"]

        messages = [{"role": "system", "content": self.system_prompt}]
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})

        await send_event({"type": "agent_active", "agent": "main"})

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=ROUTER_TOOLS,
            tool_choice="required",
        )

        message = response.choices[0].message

        if message.tool_calls:
            tool_call = message.tool_calls[0]
            tool_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            return await self._dispatch(session_id, tool_name, args, send_event)

        return message.content or "I'm not sure how to help. Could you clarify?"

    async def _dispatch(self, session_id: str, tool_name: str, args: dict, send_event) -> str:
        if tool_name == "route_to_github":
            await send_event({"type": "agent_active", "agent": "github"})
            repo_url = args.get("repo_url", "")
            return await self.github_agent.run(repo_url, send_event)

        if tool_name == "route_to_linear":
            await send_event({"type": "agent_active", "agent": "linear"})
            session_manager.update(session_id, "active_agent", "linear")
            return await self.linear_agent.run(session_id, "", send_event)

        if tool_name == "respond_directly":
            return args.get("response", "")

        return "I'm not sure how to help with that. Could you clarify?"
