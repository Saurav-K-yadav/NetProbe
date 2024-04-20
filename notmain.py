import os
import signal
import time
import getpass
import subprocess

def run_shell_script(script_path):
    try:
        subprocess.run(["bash", script_path], check=True)
        print("Shell script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_shell_script('./newscript.sh')
