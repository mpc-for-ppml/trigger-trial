import sys
import io
import time

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("🚀 Dummy task started", flush=True)
for i in range(5):
    print(f"🔧 Working... step {i+1}/5", flush=True)
    time.sleep(1)
print("✅ Dummy task complete", flush=True)
