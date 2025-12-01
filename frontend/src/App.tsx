import React, { useEffect, useState } from "react";
import Editor from "./components/Editor";

export default function App() {
  const [roomId, setRoomId] = useState<string>("");
  const [joined, setJoined] = useState(false);

  async function createRoom() {
    try {
      const res = await fetch("http://localhost:8000/rooms", { method: "POST" });
      const data = await res.json();
      setRoomId(data.roomId);
    } catch (err) {
      alert("Could not create room. Make sure backend is running.");
    }
  }

  return (
    <div style={{ padding: 20, fontFamily: "Inter, system-ui, sans-serif" }}>
      <h1>SynCode — Pair Programming</h1>

      {!joined && (
        <div style={{ marginBottom: 12 }}>
          <button onClick={createRoom}>Create Room</button>

          <input
            placeholder="Enter Room ID"
            value={roomId}
            onChange={(e) => setRoomId(e.target.value)}
            style={{ marginLeft: 8, padding: 6 }}
          />

          <button
            onClick={() => {
              if (!roomId) return alert("Please provide room id");
              setJoined(true);
            }}
            style={{ marginLeft: 8 }}
          >
            Join
          </button>
        </div>
      )}

      {joined && <Editor roomId={roomId} />}
    </div>
  );
}
