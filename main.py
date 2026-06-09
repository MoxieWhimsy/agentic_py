import argparse
import json
import os

from dotenv import load_dotenv
import lmstudio as lms

from call_function import available_functions_prompt, FunctionCall, call_function, FunctionResponse
from prompts import system_prompt
from response_parser import parse_braces_dict

load_dotenv()
api_key = os.environ.get("LM_API_TOKEN")

if api_key is None:
    raise RuntimeError("api key not loaded")

def do_one_response_round(chat: lms.Chat, model: lms.LLM, function_results: list, verbose: bool) -> lms.PredictionResult:
    # models.generate_content
    result = model.respond(chat)

    if result is None or result.stats is None:
        raise RuntimeError("model response failed")

    if 'function_call' in result.content:
        first_start = result.content.find('function_call')
        start = result.content.find('"', first_start)+1
        name = result.content[start:result.content.find('"', start)]
        start = result.content.find("{")
        arguments = parse_braces_dict(result.content[start:result.content.find("}")+1], verbose)
        function_call_result = call_function(FunctionCall(name, arguments), verbose)
        if function_call_result.parts is None or 0 == len(function_call_result.parts):
            raise Exception("function call result has no parts")

        function_response = function_call_result.parts[0]
        if function_response is None:
            raise Exception("function call result has no response")

        if function_response.response is None:
            raise Exception("function call result has no response")

        response_as_json = json.dumps(function_response.response, ensure_ascii=False)

        function_results.append(function_response.response["result"])

        chat.add_tool_result(lms.ToolCallResultData(
            content=response_as_json,
            tool_call_id=None,
        ))

        if verbose:
            print(f"-> {function_call_result.parts[0].response}")
    return result

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

    for _ in range(5):
        result = do_one_response_round(chat, model, tool_results, args.verbose)
        if args.verbose:
            print(f"Response: {result.content}\n"
                  f"Prompt tokens: {result.stats.prompt_tokens_count}\n"
                  f"Response tokens: {result.stats.predicted_tokens_count}\n")

        if not 'function_call' in result.content:
            print(result.content)
            if args.verbose:
                print(f"Tool Results:\n{'\n'.join(tool_results)}")
            exit(0)
    exit(1)



if __name__ == "__main__":
    main()
