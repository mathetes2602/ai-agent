import os
MAX_CHARS = 10000
def get_file_content(working_directory: str, file_path: str) -> str:
    try:
            
        working_directory_abspath = os.path.abspath(working_directory)
        full_file_path = os.path.join(working_directory_abspath, file_path)
        valid_file_path = os.path.commonpath([working_directory_abspath, full_file_path]) == working_directory_abspath

        if not valid_file_path:
            raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        
        if not os.path.isfile(full_file_path):
            raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')
        
        with open(full_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return content

    
    except Exception as e:
        return f"Error: {e}"
    
