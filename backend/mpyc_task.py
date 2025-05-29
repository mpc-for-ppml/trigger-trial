# mpyc_task.py
from mpyc.runtime import mpc
import argparse
import sys
import io

# Ensure UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Parse CLI arguments
parser = argparse.ArgumentParser()
parser.add_argument("--mode", type=str, default="light", choices=["light", "medium", "heavy"])
args = parser.parse_args()

def log(msg):
    print(f"[Party {mpc.pid}] {msg}", flush=True)

secint = mpc.SecInt()
step_count = {"light": 100, "medium": 500, "heavy": 1000}[args.mode]
progress_interval = step_count // 5

async def mpc_task():
    log("🚀 MPyC task started")
    log(f"🔄 Mode: {args.mode}, Steps: {step_count}")
    log("🔐 Starting secure computation...")

    await mpc.start()
        
    for i in range(step_count + 1):
        x = mpc.input(secint(i))
        y = mpc.input(secint(2 * i))
        z = await mpc.output(x + y)

        # Log progress at every 20% interval
        if i % progress_interval == 0:
            step_number = i // progress_interval + 1
            if step_number <= 5:
                log(f"🔧 Working... step {step_number}/5")

        log(f"📝 Result at step {i}: {z}")

    await mpc.shutdown()
    log("🛑 MPyC shutdown")

# Use MPyC's loop-safe runner
mpc.run(mpc_task())
log("✅ MPyC task complete")
