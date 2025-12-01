import React, { useEffect, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../store";
import { setCode, setSuggestion, clearSuggestion } from "../features/editorSlice";

export default function Editor({ roomId }: { roomId: string }) {
  const dispatch = useDispatch();
  const code = useSelector((s: RootState) => s.editor.code);
  const suggestion = useSelector((s: RootState) => s.editor.suggestion);

  const wsRef = useRef<WebSocket | null>(null);
  const debounceRef = useRef<number | undefined>(undefined);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${roomId}`);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("ws open");
    };

    ws.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        if (data.code !== undefined) {
          dispatch(setCode(data.code));
        }
      } catch (e) {
        // ignore malformed
      }
    };

    ws.onclose = () => {
      console.log("ws closed");
    };

    return () => {
      ws.close();
    };
  }, [roomId, dispatch]);

  function onChange(e: React.ChangeEvent<HTMLTextAreaElement>) {
    const newCode = e.target.value;
    dispatch(setCode(newCode));

    // send update via websocket
    try {
      wsRef.current?.send(JSON.stringify({ code: newCode }));
    } catch (err) {
      // ignore
    }

    // debounce autocomplete
    if (debounceRef.current) window.clearTimeout(debounceRef.current);
    debounceRef.current = window.setTimeout(async () => {
      if (!newCode) {
        dispatch(clearSuggestion());
        return;
      }
      try {
        const res = await fetch("http://localhost:8000/autocomplete", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ code: newCode, cursorPosition: newCode.length, language: "python" })
        });
        const data = await res.json();
        dispatch(setSuggestion(data.suggestion));
      } catch (err) {
        // ignore
      }
    }, 600);
  }

  return (
    <div>
      <h3 style={{ marginTop: 8 }}>Room: {roomId}</h3>
      <textarea
        value={code}
        onChange={onChange}
        style={{
          width: "800px",
          height: "420px",
          fontFamily: "monospace",
          fontSize: 14,
          padding: 12
        }}
      />
      {suggestion && (
        <div style={{ marginTop: 8 }}>
          <strong>Suggestion:</strong>
          <pre style={{ background: "#f3f3f3", padding: 10 }}>{suggestion}</pre>
        </div>
      )}
    </div>
  );
}
