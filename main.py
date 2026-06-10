import argparse
import json
import os

from dotenv import load_dotenv
import lmstudio as lms

from call_function import available_functions_prompt, FunctionCall, call_function, FunctionResponse, \
    function_call_format_reminder_prompt
from prompts import system_prompt
from response_parser import parse_braces_dict, get_within_curly_braces

load_dotenv()
api_key = os.environ.get("LM_API_TOKEN")

if api_key is None:
    raise RuntimeError("api key not loaded")

def do_one_response_round(chat: lms.Chat, model: lms.LLM, function_results: list, verbose: bool) -> lms.PredictionResult:
    # models.generate_content
    model_response = model.respond(chat)

    if model_response is None or model_response.stats is None:
        raise RuntimeError("model response failed")

    if verbose:
        print(f"Response: {model_response.content}\n"
              f"Prompt tokens: {model_response.stats.prompt_tokens_count}\n"
              f"Response tokens: {model_response.stats.predicted_tokens_count}\n")

    if '!!!function_call' in model_response.content:
        first_start = model_response.content.find('!!!function_call')
        start = model_response.content.find('{', first_start)
        fc_data = get_within_curly_braces(model_response.content[start:])
        fc_json = json.loads(fc_data)

        name: str = fc_json['name'] if 'name' in fc_json else ""
        arguments: dict = fc_json['args'] if 'args' in fc_json else {}
        function_call_result = call_function(FunctionCall(name, arguments), verbose)
        if function_call_result.parts is None or 0 == len(function_call_result.parts):
            raise Exception("function call result has no parts")

        function_response = function_call_result.parts[0].response
        if function_response is None:
            raise Exception("function call result has no response")

        response_as_json = json.dumps(function_response, ensure_ascii=False)

        error = function_response["error"] if "error" in function_response else ""
        result = function_response["result"] if "result" in function_response else ""

        chat.add_tool_result(lms.ToolCallResultData(
            content=response_as_json,
            tool_call_id=None,
        ))

        if verbose:
            print(f"-> {result}{('\nError: ' + error) if error else ''}")
    elif '[function_call]' in model_response.content:
        chat.add_tool_result(lms.ToolCallResultData(
            content=json.dumps({"reminder": function_call_format_reminder_prompt}, ensure_ascii=False),
            tool_call_id=None,
        ))
        if verbose:
            print("Added the following reminder to chat:")
            print(function_call_format_reminder_prompt)
        else:
            print("Function call format reminder")

    return model_response

def main():
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="user_prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    chat: lms.Chat = lms.Chat(initial_prompt=system_prompt+"\n"+available_functions_prompt)
    chat.add_user_message(args.user_prompt)

    model = lms.llm("qwen/qwen3.6-27b")

    tool_results: list = []

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(8):
        result = do_one_response_round(chat, model, tool_results, args.verbose)

        if not 'function_call' in result.content:
            print(result.content)
            exit(0)
    exit(1)



if __name__ == "__main__":
    main()
