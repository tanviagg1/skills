import { useState, useEffect, useRef, useCallback } from "react";
import type { ChatMessage, AgentType, WsEvent } from "../types";

const WS_URL = "ws://localhost:8000/ws";

function generateId() {
  return Math.random().toString(36).slice(2);
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [status, setStatus] = useState<string>("");
  const [activeAgent, setActiveAgent] = useState<AgentType>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [pendingDiagram, setPendingDiagram] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const sessionId = useRef(generateId());

  useEffect(() => {
    const ws = new WebSocket(`${WS_URL}/${sessionId.current}`);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const data: WsEvent = JSON.parse(event.data);

      if (data.type === "message" && data.role && data.content) {
        setMessages((prev) => {
          const msg: ChatMessage = {
            id: generateId(),
            role: data.role!,
            content: data.content!,
          };
          // Attach any pending diagram to the last assistant message
          if (data.role === "assistant" && pendingDiagram) {
            msg.diagram = pendingDiagram;
            setPendingDiagram(null);
          }
          return [...prev, msg];
        });
        setIsLoading(false);
        setStatus("");
      }

      if (data.type === "status") {
        setStatus(data.message || "");
      }

      if (data.type === "diagram") {
        setPendingDiagram(data.content || null);
      }

      if (data.type === "agent_active") {
        setActiveAgent(data.agent || null);
      }

      if (data.type === "done") {
        setIsLoading(false);
        setStatus("");
      }

      if (data.type === "error") {
        setMessages((prev) => [
          ...prev,
          {
            id: generateId(),
            role: "assistant",
            content: `Error: ${data.message}`,
          },
        ]);
        setIsLoading(false);
        setStatus("");
      }
    };

    ws.onclose = () => {
      setStatus("Disconnected. Please refresh.");
    };

    return () => ws.close();
  }, []);

  const sendMessage = useCallback((content: string) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return;
    setIsLoading(true);
    wsRef.current.send(JSON.stringify({ content }));
  }, []);

  return { messages, status, activeAgent, isLoading, sendMessage };
}
