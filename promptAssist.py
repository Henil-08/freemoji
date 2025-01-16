import os
import json
import argparse
from ollama import chat
from ollama import ChatResponse

def update_prompt(user_prompt: str):
    with open(
        f"{os.path.abspath(os.path.dirname(__file__))}/prompt/freemoji.md", "r"
    ) as file:
        prompt_content = file.read()

    full_prompt = prompt_content + f'\n\nUSER PROMPT: "{user_prompt}"'

    # get the (pre-made) conversation history and append the current full prompt
    json_path = f"{os.path.abspath(os.path.dirname(__file__))}/prompt/freemoji.json"

    try:
        with open(json_path, "r") as json_file:
            conversation_history = json.load(json_file)
            print("Using pre-existing conversation history")
    except FileNotFoundError:
        print("No pre existing conversation history")
        conversation_history = {"messages": []}

    conversation_history["messages"].append({"role": "user", "content": full_prompt})

    data = {
        "messages": conversation_history["messages"],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False,
    }

    ChatResponse = chat(model='llama3.1', messages=conversation_history["messages"], options={
        'temperature': 0.7,
        "max_tokens": -1
    }
    , stream=False)

    response = str(ChatResponse.message.content).replace("```", "").replace("\n", "")

    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate a refined emoji prompt.")
    parser.add_argument(
        "user_prompt", type=str, help="The user's input describing the emoji."
    )

    # Parse command-line arguments
    args = parser.parse_args()

    # Pass the user prompt to the function and print the output
    refined_prompt = update_prompt(args.user_prompt)
    print("Refined Prompt:", refined_prompt)
