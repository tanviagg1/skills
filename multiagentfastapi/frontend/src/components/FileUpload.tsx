import { useState, useRef } from "react";

const API_URL = "http://localhost:8000";

export function FileUpload() {
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setMessage(`Uploading ${file.name}...`);

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch(`${API_URL}/upload`, { method: "POST", body: form });
      const data = await res.json();

      if (data.error) {
        setMessage(`Error: ${data.error}`);
      } else {
        setMessage(`Indexed ${file.name} — ${data.chunks} chunks stored`);
      }
    } catch {
      setMessage("Upload failed. Is the backend running?");
    } finally {
      setUploading(false);
      if (inputRef.current) inputRef.current.value = "";
    }
  };

  return (
    <div style={{ padding: "8px 16px", borderTop: "1px solid #e2e8f0", background: "#f8fafc", display: "flex", alignItems: "center", gap: 10 }}>
      <label
        style={{
          cursor: uploading ? "not-allowed" : "pointer",
          padding: "5px 12px",
          background: uploading ? "#94a3b8" : "#0f172a",
          color: "#fff",
          borderRadius: 6,
          fontSize: 12,
          fontWeight: 600,
          whiteSpace: "nowrap",
        }}
      >
        {uploading ? "Uploading..." : "Upload Document"}
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.txt,.md"
          onChange={handleUpload}
          disabled={uploading}
          style={{ display: "none" }}
        />
      </label>
      {message && (
        <span style={{ fontSize: 12, color: "#64748b" }}>{message}</span>
      )}
      <span style={{ fontSize: 11, color: "#94a3b8", marginLeft: "auto" }}>PDF, TXT, MD</span>
    </div>
  );
}
