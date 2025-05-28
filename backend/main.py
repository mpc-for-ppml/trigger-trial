import os
import subprocess
import asyncio
import threading
import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
process_ref = None

# CORS setup (adjust if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "output.log")


def ensure_log_file_exists():
    os.makedirs(LOG_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("")  # create empty log file


@app.post("/run")
def run_module(background_tasks: BackgroundTasks):
    global process_ref
    print("🚀 Launching dummy_task.py")

    ensure_log_file_exists()

    def run_and_log():
        global process_ref
        with open(LOG_FILE, "w", encoding="utf-8") as logfile:
            process_ref = subprocess.Popen(
                ["python", "dummy_task.py"],
                stdout=logfile,
                stderr=logfile,
                bufsize=1,
                universal_newlines=True,
            )
            process_ref.wait()

    background_tasks.add_task(run_and_log)
    return {"status": "started"}


@app.websocket("/ws/progress")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🔌 WebSocket connected")

    try:
        # Clear the log file so frontend always gets a fresh stream
        ensure_log_file_exists()
        with open(LOG_FILE, "w", encoding="utf-8"):
            pass  # truncate file to zero length

        with open(LOG_FILE, "r", encoding="utf-8") as f:
            f.seek(0, os.SEEK_END)  # Start tailing from the end
            
            has_output = False  # Track if we have sent any output

            while True:
                line = f.readline()
                if line:
                    has_output = True
                    await websocket.send_text(line.strip())
                else:
                    await asyncio.sleep(0.5)

                # End WebSocket when dummy_task.py ends
                if process_ref and process_ref.poll() is not None and has_output:
                    await websocket.send_text("✅ Process complete")
                    await websocket.close()
                    break

    except WebSocketDisconnect:
        print("❌ WebSocket disconnected — log cleared")
    except Exception as e:
        await websocket.send_text(f"⚠️ Error: {str(e)}")
        await websocket.close()
