import subprocess

proc = subprocess.Popen(['dist/backend.exe'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
proc.stdin.write('{"action": "stats"}\n')
proc.stdin.flush()

out = proc.stdout.readline()
print("Received STDOUT:", repr(out))

stderr_out = proc.stderr.read()
print("Received STDERR:", stderr_out)

proc.kill()
