export type MessageRole = "user" | "assistant";
export type AgentType = "main" | "github" | "linear" | null;

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  diagram?: string;
}

export interface WsEvent {
  type: "message" | "status" | "diagram" | "agent_active" | "done" | "error";
  role?: MessageRole;
  content?: string;
  agent?: AgentType;
  message?: string;
}
