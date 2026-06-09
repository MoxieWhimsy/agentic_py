import argparse
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


def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="user_prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    chat: lms.Chat = lms.Chat(initial_prompt=system_prompt+"\n"+available_functions_prompt)
    chat.add_user_message(args.user_prompt)

    model = lms.llm("mistralai/devstral-small-2-2512")

    # models.generate_content
    result = model.respond(chat)

    if result is None or result.stats is None:
        raise RuntimeError("model response failed")

    if 'function_call' in result.content:
        first_start = result.content.find('function_call')
        start = result.content.find('"', first_start)+1
        name = result.content[start:result.content.find('"', start)]
        start = result.content.find("{")
        arguments = parse_braces_dict(result.content[start:result.content.find("}")+1])
        function_call_result = call_function(FunctionCall(name, arguments), args.verbose)
        if function_call_result.parts is None or 0 == len(function_call_result.parts):
            raise Exception("function call result has no parts")

        function_response = function_call_result.parts[0]
        if function_response is None:
            raise Exception("function call result has no response")

        if function_response.response is None:
            raise Exception("function call result has no response")

        function_results = [
            function_response.response,
        ]

        if args.verbose:
            print(f"-> {function_call_result.parts[0].response}")

    output = f"User prompt: {args.user_prompt}\n" \
          f"Prompt tokens: {result.stats.prompt_tokens_count}\n" \
          f"Response tokens: {result.stats.predicted_tokens_count}\n" if args.verbose else ""


    output += f"Response:\n{result.content}"
    print(output)


if __name__ == "__main__":
    main()
