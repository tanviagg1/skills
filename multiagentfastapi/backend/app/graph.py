from typing import TypedDict, Any
from pathlib import Path
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from app.config import settings
from app.session import session_manager
from app.agents.github_agent.agent import GitHubAgent
from app.agents.linear_agent.agent import LinearAgent
from app.agents.knowledge_agent.agent import KnowledgeAgent

ROUTER_PROMPT_PATH = Path(__file__).parent / "prompts" / "router.md"

# ── Tool definitions (LangChain format) ──────────────────────────────────────

ROUTER_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "route_to_github",
            "description": "Route to GitHub agent when user provides a GitHub repo URL or asks to analyse code or generate a sequence diagram.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string"},
                    "intent": {"type": "string"},
                },
                "required": ["repo_url", "intent"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "route_to_linear",
            "description": "Route to Linear agent when user wants to create a project, stories, issues or tickets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "context": {"type": "string"},
                },
                "required": ["context"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "route_to_knowledge",
            "description": "Route to Knowledge agent when user asks a question about uploaded documents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                },
                "required": ["question"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "respond_directly",
            "description": "Respond directly for greetings, capability questions, or unclear intent.",
            "parameters": {
                "type": "object",
                "properties": {
                    "response": {"type": "string"},
                },
                "required": ["response"],
            },
        },
    },
]

# ── Graph state ───────────────────────────────────────────────────────────────

class AgentState(TypedDict):
    session_id: str
    user_message: str
    active_agent: str | None   # persisted across turns for linear multi-turn
    tool_args: dict
    response: str


# ── Agent singletons ──────────────────────────────────────────────────────────

_github_agent = GitHubAgent()
_linear_agent = LinearAgent()
_knowledge_agent = KnowledgeAgent()

_llm = ChatGroq(api_key=settings.groq_api_key, model="llama-3.3-70b-versatile")
_llm_with_tools = _llm.bind_tools(ROUTER_TOOLS, tool_choice="required")

# ── Nodes ─────────────────────────────────────────────────────────────────────

async def router_node(state: AgentState, config: RunnableConfig) -> dict:
    send_event = config["configurable"]["send_event"]

    # If Linear is mid-conversation, skip routing and continue it
    if state.get("active_agent") == "linear":
        return {"active_agent": "linear", "tool_args": {}}

    await send_event({"type": "agent_active", "agent": "main"})

    system_prompt = ROUTER_PROMPT_PATH.read_text()
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["user_message"]),
    ]

    response = await _llm_with_tools.ainvoke(messages)

    if response.tool_calls:
        call = response.tool_calls[0]
        return {"active_agent": call["name"], "tool_args": call["args"]}

    return {"active_agent": "respond_directly", "tool_args": {"response": response.content}}


async def github_node(state: AgentState, config: RunnableConfig) -> dict:
    send_event = config["configurable"]["send_event"]
    await send_event({"type": "agent_active", "agent": "github"})
    repo_url = state["tool_args"].get("repo_url", "")
    response = await _github_agent.run(repo_url, send_event)
    return {"response": response, "active_agent": None}


async def linear_node(state: AgentState, config: RunnableConfig) -> dict:
    send_event = config["configurable"]["send_event"]
    await send_event({"type": "agent_active", "agent": "linear"})

    response = await _linear_agent.run(state["session_id"], state["user_message"], send_event)

    # Check if linear conversation is finished
    session = session_manager.get(state["session_id"])
    agent_state = session.get("agent_state")
    still_active = agent_state and not agent_state.is_done()

    return {
        "response": response,
        "active_agent": "linear" if still_active else None,
    }


async def knowledge_node(state: AgentState, config: RunnableConfig) -> dict:
    send_event = config["configurable"]["send_event"]
    await send_event({"type": "agent_active", "agent": "knowledge"})
    question = state["tool_args"].get("question", state["user_message"])
    response = await _knowledge_agent.query(question, send_event)
    return {"response": response, "active_agent": None}


async def direct_node(state: AgentState, config: RunnableConfig) -> dict:
    response = state["tool_args"].get("response", "How can I help you?")
    return {"response": response, "active_agent": None}


# ── Routing function ──────────────────────────────────────────────────────────

def route_decision(state: AgentState) -> str:
    agent = state.get("active_agent")
    if agent == "route_to_github":
        return "github"
    if agent in ("route_to_linear", "linear"):
        return "linear"
    if agent == "route_to_knowledge":
        return "knowledge"
    return "direct"


# ── Build graph ───────────────────────────────────────────────────────────────

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("github", github_node)
    graph.add_node("linear", linear_node)
    graph.add_node("knowledge", knowledge_node)
    graph.add_node("direct", direct_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        route_decision,
        {
            "github": "github",
            "linear": "linear",
            "knowledge": "knowledge",
            "direct": "direct",
        },
    )

    graph.add_edge("github", END)
    graph.add_edge("linear", END)
    graph.add_edge("knowledge", END)
    graph.add_edge("direct", END)

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)


# Singleton compiled graph
agent_graph = build_graph()
