import { useProgress } from "../hooks/useProgress";

export function ProgressLog() {
  const { messages } = useProgress();

  return (
    <div className="p-4 bg-gray-100 rounded-xl shadow max-w-2xl mx-auto">
        <h2 className="text-xl font-bold mb-2">🧠 Module Progress</h2>
        <div className="space-y-1 font-mono text-sm text-gray-700 max-h-80 overflow-y-auto">
            {messages.length === 0 && <div>No progress yet.</div>}
            {messages.map((msg, idx) => (
                <div key={idx}>{msg}</div>
            ))}
        </div>
    </div>
  );
}