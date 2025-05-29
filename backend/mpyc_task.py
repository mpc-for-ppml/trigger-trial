# mpyc_task.py
from mpyc.runtime import mpc
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

secint = mpc.SecInt()

async def mpc_task():
    print("🚀 MPyC task started", flush=True)
    print("🔐 Starting secure computation...", flush=True)

    await mpc.start()    
    for i in range(500):
        x = mpc.input(mpc.SecInt()(i))
        y = mpc.input(mpc.SecInt()(2 * i))
        z = await mpc.output(x + y)

        print(f"🔧 Working... step {int((i+1)/100)}/5", flush=True)
        print(f"📝 Secure result: {z}", flush=True)

    await mpc.shutdown()

mpc.run(mpc_task())  # <== THIS handles the asyncio loop correctly
print("✅ MPyC task complete", flush=True)