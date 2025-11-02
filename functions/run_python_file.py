import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=[]):
    
    try:
    
        abs_work = os.path.abspath(working_directory)
        
        if not os.path.isdir(abs_work):
            return(f"Error: \"{working_directory}\" is not a directory")
        
        target = os.path.abspath(os.path.join(abs_work, file_path))
        
        if not os.path.commonpath([abs_work, target]) == abs_work:
            return(f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory")
        
        if not os.path.exists(target):
            return(f'Error: File "{file_path}" not found.')
        
        if not target.endswith(".py"):
            return(f'Error: "{file_path}" is not a Python file.')
        
        cmd = [sys.executable, file_path, *args]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=abs_work)
        out = (result.stdout or "").strip()
        err = (result.stderr or "").strip()
        
        if out =="" and err == "":
            return f"No output produced."    
        
        parts = [f"STDOUT: {out}", f"STDERR: {err}"]

        if result.returncode != 0:
            parts.append(f"Process exited with code {result.returncode}")
        
        return " ".join(parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"