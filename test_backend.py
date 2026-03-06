import subprocess
import json

proc = subprocess.Popen(["dist/backend.exe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = proc.communicate('{"action": "lookup", "word": "carnivore", "source": "auto"}\n')
print("STDOUT:", stdout)
print("STDERR:", stderr)
