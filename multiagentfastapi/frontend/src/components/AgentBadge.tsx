import type { AgentType } from "../types";

const AGENT_LABELS: Record<string, { label: string; color: string }> = {
  main: { label: "Main Agent", color: "#6366f1" },
  github: { label: "GitHub Agent", color: "#0f172a" },
  linear: { label: "Linear Agent", color: "#5e6ad2" },
  knowledge: { label: "Knowledge Agent", color: "#0891b2" },
};

export function AgentBadge({ agent }: { agent: AgentType }) {
  if (!agent) return null;
  const config = AGENT_LABELS[agent];
  if (!config) return null;

  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 6,
        padding: "3px 10px",
        borderRadius: 12,
        background: config.color,
        color: "#fff",
        fontSize: 12,
        fontWeight: 600,
      }}
    >
      <span
        style={{
          width: 6,
          height: 6,
          borderRadius: "50%",
          background: "#fff",
          animation: "pulse 1.5s infinite",
        }}
      />
      {config.label}
    </div>
  );
}
