import subprocess
import os
import sys

def main():
    # When frozen by PyInstaller, sys.executable is the .exe itself.
    # All sibling files (Tracker.jar, backend.exe) live in the same directory.
    base_dir = os.path.dirname(os.path.abspath(
        sys.executable if getattr(sys, 'frozen', False) else __file__))
    jar_path = os.path.join(base_dir, "Tracker.jar")

    if sys.platform == "win32":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.Popen(["java", "-jar", jar_path], cwd=base_dir, startupinfo=startupinfo)
    else:
        subprocess.Popen(["java", "-jar", jar_path], cwd=base_dir)

if __name__ == "__main__":
    main()
