from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()
progress_queue = asyncio.Queue()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run")
async def run_module():
    print("✅ /run endpoint triggered")
    asyncio.create_task(simulate_steps(progress_queue))
    return {"status": "started"}

@app.websocket("/ws/progress")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🔌 WebSocket connected")

    try:
        while True:
            message = await progress_queue.get()

            if message == "__DONE__":
                print("🛑 Received DONE signal. Closing WebSocket.")
                await websocket.send_text("✅ Module complete.")
                break

            print(f"📤 Sending message: {message}")
            await websocket.send_text(message)

    except Exception as e:
        print(f"❌ WebSocket error: {e}")
    finally:
        await websocket.close()
        print("🔌 WebSocket closed")

async def simulate_steps(queue: asyncio.Queue):
    print("🧪 simulate_steps() called")
    steps = [
        "[Normalizer] 🧪 Applied 'zscore' normalization.",
        "2025-04-15 12:29:23,070 Start MPyC runtime v0.10",
        "2025-04-15 12:29:24,597 All 3 parties connected.",
        "[Party 1] ✅ Received user ID lists from all parties.",
        "[Party 1] 🔎 Computing intersection of user IDs...",
        "[Party 1] 🔗 Found 20 intersected user IDs in 77.70s",
        "[Party 1] 🧩 Filtering data for intersected user IDs...",
        "[Party 1] 📦 Filtered 20 records.",
        "[Party 1] ✅ Completed data join.",
        "[Party 1] 🧾 Final joined dataset (features + label)",
        "✅ Done!"
    ]

    for step in steps:
        await queue.put(step)
        await asyncio.sleep(1)

    await queue.put("__DONE__")
