import json
import shutil
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.graph import agent_graph
from app.agents.knowledge_agent.indexer import index_file, get_indexed_files, UPLOAD_DIR

app = FastAPI(title="Multi-Agent Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/documents")
async def list_documents():
    return {"files": get_indexed_files()}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    allowed = {".pdf", ".txt", ".md"}
    suffix = Path(file.filename).suffix.lower()

    if suffix not in allowed:
        return {"error": f"Unsupported file type. Allowed: {', '.join(allowed)}"}

    dest = UPLOAD_DIR / file.filename
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        chunks = index_file(dest)
        return {"success": True, "file": file.filename, "chunks": chunks}
    except Exception as e:
        return {"error": str(e)}


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()

    async def send_event(event: dict):
        await websocket.send_text(json.dumps(event))

    try:
        await send_event({
            "type": "message",
            "role": "assistant",
            "content": (
                "Hi! I can help you with three things:\n"
                "1. **Analyse a GitHub repo** — share a GitHub URL and I'll generate a sequence diagram\n"
                "2. **Create Linear stories** — tell me what you want to build\n"
                "3. **Answer questions from your documents** — upload a PDF or text file and ask away\n\n"
                "What would you like to do?"
            ),
        })

        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            user_message = payload.get("content", "").strip()

            if not user_message:
                continue

            await send_event({"type": "message", "role": "user", "content": user_message})

            # Run through LangGraph
            config = {
                "configurable": {
                    "thread_id": session_id,   # MemorySaver key — persists state across turns
                    "send_event": send_event,
                }
            }

            result = await agent_graph.ainvoke(
                {"session_id": session_id, "user_message": user_message},
                config=config,
            )

            response = result.get("response", "")
            if response:
                await send_event({"type": "message", "role": "assistant", "content": response})

            await send_event({"type": "done"})

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await send_event({"type": "error", "message": str(e)})
