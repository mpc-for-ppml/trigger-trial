# mpyc_task.py
from mpyc.runtime import mpc
import sys
import io

# Ensure UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def log(msg):
    print(f"[Party {mpc.pid}] {msg}", flush=True)

secint = mpc.SecInt()

async def mpc_task():
    log("🚀 MPyC task started")
    log("🔐 Starting secure computation...")

    await mpc.start()
    
    for i in range(501):
        x = mpc.input(secint(i))
        y = mpc.input(secint(2 * i))
        z = await mpc.output(x + y)

        if i % 100 == 0:
            log(f"🔧 Working... step {int((i+1)/100)}/5")
        log(f"📝 Secure result: {z}")

    await mpc.shutdown()
    log("🛑 MPyC shutdown")

# Use MPyC's loop-safe runner
mpc.run(mpc_task())
log("✅ MPyC task complete")
