import os 
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        working_directory_absolute_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_absolute_path, file_path))
        
        # Checks if the target is in the correct path, returning a false or true
        valid_target_dir = os.path.commonpath([working_directory_absolute_path, target_file_path]) == working_directory_absolute_path
        if valid_target_dir == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_path) == True:
            return f'Error: Cannot write to "{file_path}" as it is a directory' 
        
        # Checks if file path has all needed directories and creates them if needed
        target_parent_dir = os.path.dirname(target_file_path)
        os.makedirs(target_parent_dir, exist_ok=True)

        with open(target_file_path, "w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)