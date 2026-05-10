import os

def get_files_info(working_directory, directory="."):
    try:
        working_directory_absolute_path = os.path.abspath(working_directory)
        target_dir_path = os.path.normpath(os.path.join(working_directory_absolute_path, directory))
        
        # Checks if the target is in the correct path, returning a false or true
        valid_target_dir = os.path.commonpath([working_directory_absolute_path, target_dir_path]) == working_directory_absolute_path
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir_path) == False:
            return f'Error: "{directory}" is not a directory' 
        
        dir_list = os.listdir(target_dir_path)
        return_list = []
        for name in dir_list:
            full_path = os.path.join(target_dir_path, name)
            
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            
            return_list.append(f"- {name}: file_size={file_size}, is_dir={is_dir}")

        return "\n".join(return_list)
    
    except Exception as e:
        return f"Error: {e}"
    