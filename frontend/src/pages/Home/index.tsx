import { useNavigate } from "react-router-dom";
import { useState } from "react";

export function Home() {
    const [isRunning, setIsRunning] = useState(false);
    const navigate = useNavigate();

    const handleRun = async () => {
        setIsRunning(true); // Disable button immediately
        try {
            await fetch("http://localhost:8080/run", { method: "POST" });
            navigate("/log"); // Navigate to log page after starting
        } catch (err) {
        console.error("Error running module:", err);
            setIsRunning(false); // Re-enable on error
        }
    };

    return (
        <main className="p-6 flex flex-col items-center justify-center bg-white">
            <button
                onClick={handleRun}
                disabled={isRunning}
                className={`px-4 py-2 rounded-lg transition 
                ${isRunning ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700 text-white"}`}
            >
                ▶️ Run Module
            </button>
        </main>
    );
}