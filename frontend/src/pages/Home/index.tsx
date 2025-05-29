import { useNavigate } from "react-router-dom";

export function Home() {
    const navigate = useNavigate();

    return (
        <main className="p-6 flex flex-col items-center justify-center bg-white">
            <button
                onClick={() => navigate("/options")}
                className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white"
            >
                ▶️ Run Module
            </button>
        </main>
    );
}