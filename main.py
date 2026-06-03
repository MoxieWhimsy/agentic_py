import argparse
import os
from dotenv import load_dotenv
import lmstudio as lms

load_dotenv()
api_key = os.environ.get("LM_API_TOKEN")


def main():
    if api_key is None:
        raise RuntimeError("api key not loaded")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="user_prompt")
    args = parser.parse_args()

    model = lms.llm("mistralai/devstral-small-2-2512")

    prompt = args.user_prompt

    # models.generate_content
    result = model.respond(prompt)

    if result is None or result.stats is None:
        raise RuntimeError("model response failed")

    print(f"User prompt: {prompt}\n"
          f"Prompt tokens: {result.stats.prompt_tokens_count}\n"
          f"Response tokens: {result.stats.predicted_tokens_count}\n"
          f"Response:\n{result.content}")
    # model.respond result uses .content property instead of .text property


if __name__ == "__main__":
    main()
