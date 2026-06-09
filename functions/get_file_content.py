import os
from config import max_read_file_characters as MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_path = os.path.join(absolute_path, file_path)
        valid_target_path = os.path.commonpath([target_path, absolute_path]) == absolute_path
        if not valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        if valid_target_path:
            f = open(target_path, 'r')
            content = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            f.close()

            return f'SUCCESS!\n{content}'

    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = {
    "name": "get_file_content",
    "description": "Read a file's content",
    "arguments": {
        "file_path": str,
    },
    "required": ["file_path"],
}