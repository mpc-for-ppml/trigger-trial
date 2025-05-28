import { useEffect, useState } from "react";

export function useProgress() {
    const [messages, setMessages] = useState<string[]>([]);

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:8080/ws/progress");

        ws.onopen = () => console.log("✅ WebSocket connected");
        ws.onerror = (err) => console.error("❌ WebSocket error", err);
        ws.onclose = () => console.log("🔌 WebSocket closed");

        ws.onmessage = (event) => {
        console.log("📨 WebSocket message", event.data);
            setMessages((prev) => [...prev, event.data]);
        };

        return () => ws.close();
    }, []);

    return { messages };
}
