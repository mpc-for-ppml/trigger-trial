import os
import sys
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
    print("🚀 Launching 3-party MPyC task")

    ensure_log_file_exists()

    def run_and_log():
        num_parties = 3
        processes = []

        with open(LOG_FILE, "w", encoding="utf-8") as logfile:
            for i in range(num_parties):
                p = subprocess.Popen(
                    [sys.executable, "-m", "mpyc", "mpyc_task.py", "-M", str(num_parties), "-I", str(i)],
                    stdout=logfile,
                    stderr=logfile,
                    bufsize=1,
                    universal_newlines=True,
                )
                processes.append(p)

            for p in processes:
                p.wait()

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
            milestone_final = "✅ MPyc task complete"
            sent_final = False

            while True:            
                line = f.readline()
                if line:
                    cleaned_line = line.strip()
                    await websocket.send_text(cleaned_line)
                    has_output = True

                    if cleaned_line == milestone_final:
                        sent_final = True
                else:
                    await asyncio.sleep(0.5)

                # End WebSocket when dummy_task.py ends
                if process_ref and process_ref.poll() is not None and has_output and sent_final:
                    await websocket.send_text("🛑 MPyC shutdown")
                    await websocket.close()
                    break

    except WebSocketDisconnect:
        print("❌ WebSocket disconnected — log cleared")
    except Exception as e:
        await websocket.send_text(f"⚠️ Error: {str(e)}")
        await websocket.close()
