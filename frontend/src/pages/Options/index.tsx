// pages/Options/index.tsx
import { useNavigate } from "react-router-dom";
import { useState } from "react";

export function Options() {
    const navigate = useNavigate();
    const [selectedOption, setSelectedOption] = useState<string>();

    const runWithOption = async () => {
        try {
            await fetch("http://localhost:8080/run", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ mode: selectedOption }),
            });
            navigate("/log");
        } catch (err) {
            console.error("Error starting task:", err);
        }
    };

    return (
        <main className="min-h-screen flex flex-col items-center justify-center gap-6 p-6 bg-white">
            <h2 className="text-xl font-semibold">Select Processing Mode</h2>
            <div className="flex gap-4">
                {["light", "medium", "heavy"].map((option) => (
                <button
                    key={option}
                    onClick={() => setSelectedOption(option)}
                    className={`px-4 py-2 rounded-lg ${
                        selectedOption === option ? "bg-blue-700 text-white" : "bg-gray-300"
                    }`}
                >
                    {option}
                </button>
                ))}
            </div>
            <button
                onClick={runWithOption}
                disabled={!selectedOption}
                className={`mt-4 px-4 py-2 rounded-lg ${
                selectedOption ? "bg-green-600 text-white" : "bg-gray-400 cursor-not-allowed"
                }`}
            >
                ▶️ Run Task
            </button>
        </main>
    );
}
