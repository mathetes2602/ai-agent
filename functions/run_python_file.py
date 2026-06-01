import os
import subprocess
from google.genai import types

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_directory_abspath = os.path.abspath(working_directory)
        file_abspath = os.path.normpath(os.path.join(working_directory_abspath, file_path))

        if os.path.commonpath([working_directory_abspath, file_abspath]) != working_directory_abspath:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(file_abspath):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_abspath.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", file_abspath]
        if args:
            command.extend(args)

        subprocess_result = subprocess.run(args=command, cwd=working_directory_abspath, capture_output=True, text=True, timeout=30,)

        if subprocess_result.returncode != 0:
            return f"Process exited with code {subprocess_result.returncode}"
        
        if not subprocess_result.stdout and not subprocess_result.stderr:
            return f"No output produced"
        
        return f"STDOUT: {subprocess_result.stdout}\nSTDERR: {subprocess_result.stderr}"
    except Exception as e:
        print(f"Error: executing Python file: {e}")

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Runs the specified python file",
            ),
            "args": types.Schema(
                type= types.Type.ARRAY,
                description="List of string arguents that we want to pass to the program that we run",
                items= types.Schema(
                    type= types.Type.STRING,
                    description="A string argument that we pass to the program we are trying to run"
                )
            )
        },
        required=["file_path"]
    ),
)