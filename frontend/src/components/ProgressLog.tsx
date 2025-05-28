import { useProgress } from "../hooks/useProgress";

const milestones = [
    "🚀 Dummy task started",
    "🔧 Working... step 1/5",
    "🔧 Working... step 2/5",
    "🔧 Working... step 3/5",
    "🔧 Working... step 4/5",
    "🔧 Working... step 5/5",
    "✅ Dummy task complete",
];

export function ProgressLog() {
    const { messages } = useProgress();

    // Check which milestones have been reached
    const reached = milestones.map((milestone) =>
        messages.includes(milestone)
    );

    return (
        <div className="p-4 bg-gray-100 rounded-xl shadow max-w-3xl mx-auto w-full text-black">
            <h2 className="text-xl font-bold mb-4">🧠 Module Progress</h2>

            {/* Horizontal Progress Bar */}
            <div className="relative flex items-center justify-between w-full mb-6 px-3">
                {/* Connector Line Behind Dots */}
                <div className="absolute top-3 left-6 right-6 h-0.5 z-0 flex">
                    {milestones.slice(1).map((_, idx) => (
                        <div
                            key={idx}
                            className={`flex-1 transition-all ${
                                reached[idx + 1] ? "bg-blue-600" : "bg-gray-300"
                        }`}
                        />
                    ))}
                </div>

                {/* Milestones */}
                {milestones.map((milestone, idx) => (
                    <div key={milestone} className="relative z-10 flex flex-col items-center flex-1 text-center">
                        {/* Dot */}
                        <div
                            className={`w-6 h-6 rounded-full border-2 transition-all
                                ${reached[idx] ? "bg-blue-600 border-blue-600" : "bg-white border-gray-300"}
                                ${reached[idx] && !reached[idx + 1] ? "scale-110 shadow" : ""}
                            `}
                        />
                        {/* Label */}
                        <span className="text-xs mt-2 max-w-[80px] break-words">
                            {milestone.replace("🔧 ", "").replace("🚀 ", "").replace("✅ ", "")}
                        </span>
                    </div>
                ))}
            </div>

            {/* Optional Raw Logs */}
            <div className="space-y-1 font-mono text-sm text-gray-700 max-h-40 overflow-y-auto">
                {messages.length === 0 && <div>No progress yet.</div>}
                {messages.map((msg, idx) => (
                    <div key={idx}>{msg}</div>
                ))}
            </div>
        </div>
    );
}
