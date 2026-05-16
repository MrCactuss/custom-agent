import os
import subprocess 
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_absolute_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_absolute_path, file_path))
        
        # Checks if the target is in the correct path, returning a false or true
        valid_target_dir = os.path.commonpath([working_directory_absolute_path, target_file_path]) == working_directory_absolute_path
        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file_path) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if target_file_path[-2:] != "py":
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_path]

        if args != None:
            command.append(args)

        process_object = subprocess.run(command, capture_output=True, text=True, timeout=30, cwd=working_directory_absolute_path)

        if process_object.returncode != 0:
            return f'Process exited with code {process_object.returncode}'
        elif process_object.stderr == None and process_object.stdout == None:
            return f'No output produced'
        else:
            return f"STDOUT: {process_object.stdout}, STDERR: {process_object.stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified directory with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)