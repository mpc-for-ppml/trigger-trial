import os
import platform
import subprocess
import asyncio
import psutil
import threading
import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

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
def run_module():
    print("🚀 Starting dummy_task.py in new terminal with logging")

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    if platform.system() == "Windows":
        subprocess.Popen(
            ["cmd", "/c", f"python dummy_task.py >> {LOG_FILE} 2>&1"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    elif platform.system() == "Linux":
        subprocess.Popen(
            ["gnome-terminal", "--", "bash", "-c", f"python3 dummy_task.py >> {LOG_FILE} 2>&1; exec bash"]
        )
    elif platform.system() == "Darwin":
        subprocess.Popen(
            ["osascript", "-e", f'tell app "Terminal" to do script "python3 dummy_task.py >> {LOG_FILE} 2>&1"']
        )
    else:
        return {"error": "Unsupported OS"}

    return {"status": "started"}


@app.websocket("/ws/progress")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("🔌 WebSocket connected")

    try:
        ensure_log_file_exists()

        with open(LOG_FILE, "r", encoding="utf-8") as f:
            f.seek(0, os.SEEK_END)  # Move to end of file

            while True:
                line = f.readline()
                if line:
                    await websocket.send_text(line.strip())
                else:
                    await asyncio.sleep(0.5)  # Wait briefly before checking again

                # Optional: stop after inactivity
                if not is_process_running("dummy_task.py"):
                    await websocket.send_text("✅ Process complete")
                    await websocket.close()
                    break

    except WebSocketDisconnect:
        print("❌ WebSocket disconnected")
    except Exception as e:
        await websocket.send_text(f"⚠️ Error: {str(e)}")
        await websocket.close()


@app.post("/run")
def run_module():
    print("🚀 Starting dummy_task.py in new terminal with logging")

    # Ensure log file directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    if platform.system() == "Windows":
        subprocess.Popen(
            ["start", "cmd", "/k", f"python dummy_task.py >> {LOG_FILE} 2>&1"],
            shell=True
        )
    elif platform.system() == "Linux":
        subprocess.Popen(
            ["gnome-terminal", "--", "bash", "-c", f"python3 dummy_task.py >> {LOG_FILE} 2>&1; exec bash"]
        )
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(
            ["osascript", "-e", f'tell app "Terminal" to do script "python3 dummy_task.py >> {LOG_FILE} 2>&1"']
        )
    else:
        return {"error": "Unsupported OS"}

    return {"status": "started"}


def is_process_running(script_name: str):
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            cmdline = proc.info.get("cmdline")
            if cmdline and isinstance(cmdline, list) and script_name in " ".join(cmdline):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False