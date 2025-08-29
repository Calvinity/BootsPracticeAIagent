import os
import sys
import subprocess
import requests
from google.genai import types
from .config import MAX_CHARS




schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python file in the working directory with optional args.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file, relative to the working directory (e.g. 'tests.py').",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of arguments to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)




def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []

    abs_base = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))

    if not (abs_target == abs_base or abs_target.startswith(abs_base + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(os.path.join(working_directory, file_path)):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(
            [sys.executable, file_path] + args,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=working_directory,
        )
        if not result.stdout and not result.stderr:
            return "No output produced."
        output = f"STDOUT: {result.stdout} STDERR: {result.stderr}"
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}"
        return output
    except Exception as e:
        return f"Error: {e}"