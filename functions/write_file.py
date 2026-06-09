import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        absolute_path = os.path.abspath(working_directory)
        target_path = os.path.join(absolute_path, file_path)
        valid_target_path = os.path.commonpath([target_path, absolute_path]) == absolute_path
        if not valid_target_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        directory = os.path.dirname(target_path)
        print(f"Writing to directory {directory}")
        os.makedirs(directory, exist_ok=True)

        with open(target_path, "w") as file:
            file.write(content)
        file.close()

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'

schema_write_file = {
    "name": "write_file",
    "description": "Write content to a file",
    "arguments": {
        "file_path": str,
        "content": str
    },
    "required": ["file_path", "content"],
}