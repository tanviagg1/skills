from typing import Any


class SessionManager:
    def __init__(self):
        self._sessions: dict[str, dict] = {}

    def get(self, session_id: str) -> dict:
        if session_id not in self._sessions:
            self._sessions[session_id] = {
                "history": [],
                "agent_state": None,
                "active_agent": None,
            }
        return self._sessions[session_id]

    def update(self, session_id: str, key: str, value: Any):
        session = self.get(session_id)
        session[key] = value

    def append_message(self, session_id: str, role: str, content: str):
        session = self.get(session_id)
        session["history"].append({"role": role, "content": content})

    def clear(self, session_id: str):
        if session_id in self._sessions:
            del self._sessions[session_id]


session_manager = SessionManager()
