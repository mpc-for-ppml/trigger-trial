import { ProgressLog } from "./components/ProgressLog";

function App() {
  const handleRun = async () => {
    await fetch("http://localhost:8080/run", {
      method: "POST",
    });
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center gap-6 p-6 bg-white">
      <button
        onClick={handleRun}
        className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
      >
        ▶️ Run Module
      </button>
      <ProgressLog />
    </main>
  );
}

export default App;
