import os


def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.join(absolute_path, directory)
        absolute_target_dir = os.path.abspath(target_dir)
        valid_target_dir = os.path.commonpath([absolute_target_dir, absolute_path]) == absolute_path
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        result = f'Success: "{directory}" is within the working directory'
        dir_list = os.listdir(target_dir)
        for short_path in dir_list:
            full_path = os.path.join(target_dir, short_path)
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            result += f'\n  - {short_path}: file_size={file_size} is_dir={is_dir}'
            pass
        return result

    except Exception as e:
        return f'Error: {e}'

schema_get_files_info = {
    "name": "get_files_info",
    "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status. Do not use this function to run Python files",
    "arguments": {
        "directory": str,
    },
    "required": ["directory"],
}