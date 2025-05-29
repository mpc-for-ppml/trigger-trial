import { useState } from "react";
import { ProgressLog } from "./components/ProgressLog";

function App() {
  const [isRunning, setIsRunning] = useState(false);

  const handleRun = async () => {
    setIsRunning(true); // Disable button immediately
    try {
      await fetch("http://localhost:8080/run", {
        method: "POST",
      });
    } catch (err) {
      console.error("Error running module:", err);
      setIsRunning(false); // Re-enable on error if needed
    }
  };

  return (
    <main className="min-h-screen min-w-screen flex flex-col items-center justify-center gap-6 p-6 bg-white">
      <button
        onClick={handleRun}
        disabled={isRunning}
        className={`px-4 py-2 rounded-lg transition 
          ${isRunning ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700 text-white"}`}
      >
        ▶️ Run Module
      </button>
      <ProgressLog />
    </main>
  );
}

export default App;
