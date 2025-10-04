import os
import json
import argparse
from mlx_lm import generate

def build_conversation_messages(user_prompt: str):
    """Build the messages array with conversation history"""
    with open(
        f"{os.path.abspath(os.path.dirname(__file__))}/prompt/freemoji.md", "r"
    ) as file:
        prompt_content = file.read()

    full_prompt = prompt_content + f'\n\nUSER PROMPT: "{user_prompt}"'
    
    # Load conversation history
    json_path = f"{os.path.abspath(os.path.dirname(__file__))}/prompt/freemoji.json"
    
    try:
        with open(json_path, "r") as json_file:
            conversation_history = json.load(json_file)
            print("Using pre-existing conversation history")
    except FileNotFoundError:
        print("No pre-existing conversation history")
        conversation_history = {"messages": []}
    
    # Append current prompt to history
    messages = conversation_history["messages"].copy()
    messages.append({"role": "user", "content": full_prompt})
    
    return messages

def update_prompt_mlx(llm, tokenizer, user_prompt: str):
    """Use MLX for macOS Metal acceleration"""
    
    # Get conversation messages
    messages = build_conversation_messages(user_prompt)
    
    # Apply chat template to format messages properly
    formatted_prompt = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=False
    )
    
    # Generate response
    print("Generating response...")
    response = generate(
        llm,
        tokenizer,
        prompt=formatted_prompt,
        max_tokens=512,
    )
    
    # Extract only the new response (after the formatted prompt)
    if formatted_prompt in response:
        response = response[len(formatted_prompt):].strip()

    # Clean response
    cleaned_response = response.replace("```", "").replace("\n", "")
    return cleaned_response

def update_prompt_vllm(llm, user_prompt: str):
    """Use vLLM for CUDA/CPU"""
    
    # Get conversation messages
    messages = build_conversation_messages(user_prompt)
    
    # Sampling parameters
    sampling_params = SamplingParams(
        temperature=0.7,
        max_tokens=512,
        stop=["\n\n"]
    )
    
    # Generate
    print("Generating response...")
    outputs = llm.chat(messages=[messages], sampling_params=sampling_params)
    response = outputs[0].outputs[0].text
    
    # Clean response
    cleaned_response = response.replace("```", "").replace("\n", "")
    return cleaned_response

def update_prompt(user_prompt: str, device_type: str, llm=None, tokenizer=None):
    """Main function to update prompt with a pre-loaded model."""
    print(f"Updating prompt with {device_type} backend...")
    if device_type == "mac":
        return update_prompt_mlx(llm, tokenizer, user_prompt)
    elif device_type == "win/linux":
        return update_prompt_vllm(llm, user_prompt)
    else:
        raise ValueError(f"Unknown backend: {device_type}")