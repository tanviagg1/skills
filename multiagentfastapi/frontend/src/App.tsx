import { useEffect, useRef } from "react";
import { useChat } from "./hooks/useChat";
import { Message } from "./components/Message";
import { InputBar } from "./components/InputBar";
import { AgentBadge } from "./components/AgentBadge";

export default function App() {
  const { messages, status, activeAgent, isLoading, sendMessage } = useChat();
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, status]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        maxWidth: 800,
        margin: "0 auto",
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: "16px 20px",
          borderBottom: "1px solid #e2e8f0",
          background: "#fff",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <div>
          <h1 style={{ margin: 0, fontSize: 18, fontWeight: 700, color: "#1e293b" }}>
            Multi-Agent Assistant
          </h1>
          <p style={{ margin: 0, fontSize: 12, color: "#64748b" }}>
            GitHub analyser + Linear story creator
          </p>
        </div>
        <AgentBadge agent={activeAgent} />
      </div>

      {/* Messages */}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "16px 20px",
          background: "#f8fafc",
        }}
      >
        {messages.map((msg) => (
          <Message key={msg.id} message={msg} />
        ))}

        {/* Status indicator */}
        {status && (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 8,
              color: "#64748b",
              fontSize: 13,
              fontStyle: "italic",
              marginBottom: 8,
            }}
          >
            <span style={{ animation: "spin 1s linear infinite", display: "inline-block" }}>⟳</span>
            {status}
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <InputBar onSend={sendMessage} disabled={isLoading} />

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.4; }
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        * { box-sizing: border-box; }
        body { margin: 0; }
      `}</style>
    </div>
  );
}
