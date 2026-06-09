from collections.abc import Callable

from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

available_functions: list[dict] = [
    schema_get_file_content,
    schema_get_files_info,
    schema_run_python_file,
    schema_write_file,
]

function_map: dict[str, Callable[..., str]] = {
    schema_get_file_content['name']: get_file_content,
    schema_get_files_info['name']: get_files_info,
    schema_run_python_file['name']: run_python_file,
    schema_write_file['name']: write_file,
}

available_functions_prompt = """
function calls begin with the literal [function_call] followed by the name of the function in quotes followed by any arguments in curly braces. 
function call format:
[function_call] "<function name>" {<arguments as key-value pairs (e.g 'arg1': 'value1', 'arg2': 'value2')>}
    
""" + f'{len(available_functions)} available functions:\n{",\n".join(map(str,available_functions))}'

class FunctionCall:
    name: str
    args: dict | None
    def __init__(self, function_name: str, args: dict | None) -> None:
        self.name = function_name
        self.args = args

class FunctionResponse:
    name: str | None
    parts: list[dict] | None
    response: dict[str, object] | None
    def __init__(self, name: str, response: dict[str, object], parts: list[dict] | None = None) -> None:
        self.name = name
        self.parts = parts
        self.response = response

class Content:
    role: str
    parts: list | None
    def __init__(self, role: str, parts: list | None = None):
        self.role = role
        self.parts = parts

def get_schema(function_name: str) -> dict | None:
    for schema in available_functions:
        if function_name != schema["name"]:
            continue
        return schema
    return None

def call_function(
    function_call: FunctionCall, verbose: bool = False
) -> Content:
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_name = function_call.name or ""
    if not (function_name in function_map):
        return Content(
            role="tool",
            parts=[{"error": f"Unknown function: {function_name}"},]
        )

    args = dict(function_call.args) if function_call.args else {}

    schema = get_schema(function_name)
    if schema is None:
        return Content(
            role="tool",
            parts=[{"error": f"Unknown schema on function: {function_name}"}, ]
        )

    for required_arg in schema["required"]:
        if required_arg not in args:
            return Content(
                role="tool",
                parts=[{"error": f"Missing required argument: {required_arg}"}, ]
            )

    for check_arg in args:
        if check_arg not in schema["arguments"]:
            return Content(
                role="tool",
                parts=[{"error": f"Unexpected argument found while calling {function_name}: {check_arg}"}, ]
            )


    args["working_directory"] = "./calculator"

    function_result = function_map[function_call.name](**args)

    return Content(
        role="tool",
        parts=[
            FunctionResponse(
                name=function_name,
                response={"result": function_result},
            ),
        ]
    )