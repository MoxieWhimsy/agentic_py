import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        absolute_working_directory_path = os.path.abspath(working_directory)
        absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        valid_target_path = os.path.commonpath([absolute_file_path, absolute_working_directory_path]) == absolute_working_directory_path
        if not valid_target_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_file_path]
        if args is not None:
            command.extend(args)

    except Exception as e:
        return f"Error: {e}"

    try:
        run_result: list[str] = list([])
        run_result.append(f"Running Python file: {file_path}")
        completed_process = subprocess.run(command, capture_output=True, timeout=30, check=True, cwd=absolute_working_directory_path, text=True)
        if completed_process.returncode != 0:
            run_result.append(f"Process exited with code {completed_process.returncode}")

        if completed_process.stderr is None and completed_process.stdout is None:
            run_result.append("No output produced")

        else:
            if 0 != len(completed_process.stdout):
                run_result.append(f"STDOUT:\n{completed_process.stdout}")
            if completed_process.stderr is not None and 0 != len(completed_process.stderr):
                run_result.append(f"STDERR:\n{completed_process.stderr}")

        return '\n'.join(run_result)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "name": "run_python_file",
    "description": "Run the specified Python (.py) file in a specified directory relative to the working directory. Works with or without arguments.",
    "arguments": {
        "file_path": str,
        "args": list[str] | None
    },
    "required": ["file_path"],
    "optional": {
        "args": str,
    },
}