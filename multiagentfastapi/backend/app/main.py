import json
import uuid
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.orchestrator import Orchestrator

app = FastAPI(title="Multi-Agent Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()

    async def send_event(event: dict):
        await websocket.send_text(json.dumps(event))

    try:
        # Send welcome message on connect
        await send_event({
            "type": "message",
            "role": "assistant",
            "content": "Hi! I can help you with two things:\n"
                       "1. **Analyse a GitHub repo** — share a GitHub URL and I'll generate a sequence diagram\n"
                       "2. **Create Linear stories** — tell me what you want to build and I'll set up your project\n\n"
                       "What would you like to do?"
        })

        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            user_message = payload.get("content", "").strip()

            if not user_message:
                continue

            # Echo user message back (for UI confirmation)
            await send_event({"type": "message", "role": "user", "content": user_message})

            # Process through orchestrator
            response = await orchestrator.handle(session_id, user_message, send_event)

            if response:
                await send_event({"type": "message", "role": "assistant", "content": response})

            await send_event({"type": "done"})

    except WebSocketDisconnect:
        pass
    except Exception as e:
        await send_event({"type": "error", "message": str(e)})
