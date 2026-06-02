import { useState } from "react";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    const response = await fetch(
      `http://127.0.0.1:8000/chat-stream?question=${encodeURIComponent(input)}&session_id=user1`
    );

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let botText = "";

    setMessages((prev) => [...prev, { role: "bot", text: "" }]);

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      botText += decoder.decode(value);
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = { role: "bot", text: botText };
        return updated;
      });
    }

    setLoading(false);
  };

  return (
    <div style={{ maxWidth: "600px", margin: "40px auto", fontFamily: "Arial" }}>
      <h2>Support Agent</h2>
      <div style={{ border: "1px solid #ccc", borderRadius: "8px", padding: "16px", height: "400px", overflowY: "auto", marginBottom: "16px" }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.role === "user" ? "right" : "left", margin: "8px 0" }}>
            <span style={{ background: msg.role === "user" ? "#0084ff" : "#f0f0f0", color: msg.role === "user" ? "white" : "black", padding: "8px 12px", borderRadius: "16px", display: "inline-block", maxWidth: "80%" }}>
              {msg.text}
            </span>
          </div>
        ))}
        {loading && <p style={{ color: "#999" }}>Typing...</p>}
      </div>
      <div style={{ display: "flex", gap: "8px" }}>
        <input
          style={{ flex: 1, padding: "10px", borderRadius: "8px", border: "1px solid #ccc" }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask a question..."
        />
        <button
          style={{ padding: "10px 20px", borderRadius: "8px", background: "#0084ff", color: "white", border: "none", cursor: "pointer" }}
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default App;