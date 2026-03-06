import subprocess
proc = subprocess.run(['python', 'backend/bridge.py'], capture_output=True, text=True)
print("STDERR:")
print(proc.stderr)
