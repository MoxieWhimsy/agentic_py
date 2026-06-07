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

        if valid_target_dir:
            return f'Success: "{directory}" is within the working directory'

    except Exception as e:
        return f'Error: {e}'