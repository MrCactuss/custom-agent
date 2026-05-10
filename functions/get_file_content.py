import os 
from config import MAX_CHARS
 
def get_file_content(working_directory, file_path):
    try:
        working_directory_absolute_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_directory_absolute_path, file_path))
        
        # Checks if the target is in the correct path, returning a false or true
        valid_target_dir = os.path.commonpath([working_directory_absolute_path, target_file_path]) == working_directory_absolute_path
        if valid_target_dir == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_file_path) == False:
            return f'Error: "{file_path}" is not a file' 

        with open(target_file_path) as file:
            read_file_string = file.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if file.read(1):
                read_file_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return read_file_string

    except Exception as e:
        return f"Error: {e}"