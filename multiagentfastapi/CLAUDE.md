# multiagentfastapi — Project Context for Claude

## What this project is
A multi-agent chatbot with a React frontend and FastAPI backend. The user types a message and an LLM-powered orchestrator (LangGraph) routes it to the right agent automatically.

## GitHub Repo
https://github.com/tanviagg1/multitaskagent
- `master` — stable code
- `langgraph-multitask-agent` — active development branch
- `feature1` — initial commit branch

## How to run
```bash
# Backend (Terminal 1)
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Frontend (Terminal 2)
cd frontend
npm run dev
# Open http://localhost:5173
```

## Project structure
```
multiagentfastapi/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, WebSocket /ws/{session_id}, POST /upload
│   │   ├── config.py            # Loads env vars (GROQ_API_KEY, GITHUB_TOKEN, LINEAR_API_KEY)
│   │   ├── session.py           # In-memory session store
│   │   ├── graph.py             # LangGraph orchestrator — routes to 3 agents
│   │   ├── agents/
│   │   │   ├── github_agent/    # Fetches GitHub repo, generates Mermaid sequence diagram
│   │   │   │   ├── agent.py
│   │   │   │   ├── analyzer.py  # Scores + picks key files
│   │   │   │   └── client.py    # PyGitHub wrapper
│   │   │   ├── linear_agent/    # Multi-turn conversation → creates Linear project + stories
│   │   │   │   ├── agent.py
│   │   │   │   ├── client.py    # Linear GraphQL API
│   │   │   │   └── collector.py # StoryCollector state machine
│   │   │   └── knowledge_agent/ # RAG agent — answers questions from uploaded docs
│   │   │       ├── agent.py     # LangChain RAG chain
│   │   │       ├── indexer.py   # Load, chunk, embed, store documents
│   │   │       └── vectorstore.py # ChromaDB singleton + HuggingFace embeddings
│   │   └── prompts/
│   │       ├── router.md        # LangGraph router system prompt
│   │       ├── github.md        # GitHub agent system prompt
│   │       └── linear.md        # Linear agent system prompt
│   ├── chroma_db/               # ChromaDB persisted vector store (created at runtime)
│   ├── uploads/                 # Uploaded files (created at runtime)
│   ├── venv/                    # Python virtual environment
│   ├── pyproject.toml
│   └── .env                     # API keys (not committed)
├── frontend/
│   └── src/
│       ├── App.tsx
│       ├── types.ts
│       ├── hooks/useChat.ts     # WebSocket connection + message state
│       └── components/
│           ├── Message.tsx
│           ├── InputBar.tsx
│           ├── AgentBadge.tsx   # Shows active agent in header
│           ├── DiagramView.tsx  # Renders Mermaid diagrams inline
│           └── FileUpload.tsx   # Upload PDF/TXT/MD to knowledge agent
└── docker-compose.yml
```

## Tech stack
| Layer | Tech |
|---|---|
| Frontend | React 19 + Vite + TypeScript |
| Backend | FastAPI + Python 3.14 |
| LLM | Groq — llama-3.3-70b-versatile |
| Orchestration | LangGraph (StateGraph + MemorySaver) |
| RAG | LangChain + ChromaDB + HuggingFace all-MiniLM-L6-v2 (local embeddings) |
| GitHub API | PyGitHub |
| Linear API | GraphQL via httpx |
| Real-time | WebSockets |

## Agents

### 1. GitHub Agent
- Triggered by: GitHub URL or request to analyse code / generate diagram
- Flow: fetch repo tree → score + pick key files → send to Groq → extract Mermaid diagram → send to frontend
- Output: sequence diagram rendered inline via Mermaid.js

### 2. Linear Agent
- Triggered by: request to create project, stories, issues, tickets
- Flow: multi-turn conversation using StoryCollector state machine
  - States: GATHERING_PROJECT_NAME → GATHERING_PROJECT_DESC → GATHERING_TEAM → GATHERING_STORIES → CONFIRMING → DONE
- Output: creates project + stories in Linear via GraphQL API

### 3. Knowledge Agent (RAG)
- Triggered by: questions about uploaded documents
- Flow: upload file → chunk (500 tokens, 50 overlap) → embed (HuggingFace local) → store in ChromaDB → on query: retrieve top 4 chunks → Groq LLM answers
- Supported file types: PDF, TXT, MD
- Embeddings model: all-MiniLM-L6-v2 (downloaded once, ~80MB, runs locally)

## LangGraph flow
```
User message → router node (Groq decides)
    → github node → END
    → linear node → END (or loops back if conversation ongoing)
    → knowledge node → END
    → direct node → END
```
MemorySaver persists `active_agent` across turns (needed for Linear multi-turn).

## API Keys (backend/.env)
```
GROQ_API_KEY=gsk_...
GITHUB_TOKEN=ghp_...
LINEAR_API_KEY=lin_api_...
```

## Known issues fixed
- `langchain.text_splitter` → `langchain_text_splitters`
- `get_vectorstore()` was not a singleton — caused indexing and querying to use separate instances
- RAG chain was too complex — simplified to direct prompt | llm | parser chain
- Frontend: `import type` required for type-only imports (verbatimModuleSyntax: true)
- Gemini free tier quota exhausted → switched to Groq
- google.generativeai deprecated → switched to google.genai (then dropped for Groq)

## WebSocket event types
```
{ type: "message", role: "user"|"assistant", content: "..." }
{ type: "status", message: "..." }           # progress updates
{ type: "diagram", content: "<mermaid>" }    # triggers DiagramView
{ type: "agent_active", agent: "main"|"github"|"linear"|"knowledge" }
{ type: "done" }
{ type: "error", message: "..." }
```
