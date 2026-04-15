import { useEffect, useRef } from "react";
import mermaid from "mermaid";

mermaid.initialize({ startOnLoad: false, theme: "default" });

let diagramCount = 0;

export function DiagramView({ diagram }: { diagram: string }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const idRef = useRef(`diagram-${++diagramCount}`);

  useEffect(() => {
    if (!containerRef.current || !diagram) return;

    mermaid
      .render(idRef.current, diagram)
      .then(({ svg }) => {
        if (containerRef.current) {
          containerRef.current.innerHTML = svg;
        }
      })
      .catch((err) => {
        if (containerRef.current) {
          containerRef.current.innerHTML = `<pre style="color:red">Diagram error: ${err.message}</pre>`;
        }
      });
  }, [diagram]);

  return (
    <div style={{ marginTop: 12 }}>
      <div
        ref={containerRef}
        style={{
          background: "#f8fafc",
          border: "1px solid #e2e8f0",
          borderRadius: 8,
          padding: 16,
          overflowX: "auto",
        }}
      />
      <button
        onClick={() => navigator.clipboard.writeText(diagram)}
        style={{
          marginTop: 6,
          fontSize: 12,
          color: "#6366f1",
          background: "none",
          border: "none",
          cursor: "pointer",
          padding: 0,
        }}
      >
        Copy Mermaid source
      </button>
    </div>
  );
}
