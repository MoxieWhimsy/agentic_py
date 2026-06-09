import argparse
import os
from dotenv import load_dotenv
from google.genai import types
import lmstudio as lms

from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("LM_API_TOKEN")

if api_key is None:
    raise RuntimeError("api key not loaded")


def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="user_prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
    ]

    chat: lms.Chat = lms.Chat(initial_prompt=system_prompt)
    chat.add_user_message(args.user_prompt)

    model = lms.llm("mistralai/devstral-small-2-2512")

    prompt = args.user_prompt

    # models.generate_content
    result = model.respond(chat)


    if result is None or result.stats is None:
        raise RuntimeError("model response failed")


    output = f"User prompt: {prompt}\n" \
          f"Prompt tokens: {result.stats.prompt_tokens_count}\n" \
          f"Response tokens: {result.stats.predicted_tokens_count}\n" if args.verbose else ""

    # model.respond result uses .content property instead of .text property
    output += f"Response:\n{result.content}"
    print(output)


if __name__ == "__main__":
    main()
