import { useState, KeyboardEvent } from "react";

interface Props {
  onSend: (message: string) => void;
  disabled: boolean;
}

export function InputBar({ onSend, disabled }: Props) {
  const [value, setValue] = useState("");

  const handleSend = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div
      style={{
        display: "flex",
        gap: 8,
        padding: "12px 16px",
        borderTop: "1px solid #e2e8f0",
        background: "#fff",
      }}
    >
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Type a message... (Enter to send, Shift+Enter for new line)"
        rows={2}
        disabled={disabled}
        style={{
          flex: 1,
          resize: "none",
          border: "1px solid #cbd5e1",
          borderRadius: 8,
          padding: "8px 12px",
          fontSize: 14,
          fontFamily: "inherit",
          outline: "none",
          lineHeight: 1.5,
        }}
      />
      <button
        onClick={handleSend}
        disabled={disabled || !value.trim()}
        style={{
          padding: "8px 20px",
          background: disabled || !value.trim() ? "#94a3b8" : "#6366f1",
          color: "#fff",
          border: "none",
          borderRadius: 8,
          cursor: disabled || !value.trim() ? "not-allowed" : "pointer",
          fontWeight: 600,
          fontSize: 14,
          alignSelf: "flex-end",
        }}
      >
        Send
      </button>
    </div>
  );
}
