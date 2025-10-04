import streamlit as st
from promptAssist import update_prompt
from generate import generate_image
from PIL import Image 
from utils import get_unique_path, get_device_config
import os
from mlx_lm import load
from vllm import LLM
from mflux import Flux1, ModelConfig
from diffusers import FluxPipeline

def load_models():
    """
    Detects the device and loads the appropriate LLM and image generation models once per session.
    """
    device_type, device = get_device_config()
    st.session_state.device_type = device_type
    st.session_state.device = device
    
    print(f"Detected device: {device_type} on {device or 'Metal'}")

    # Load the Image Generation Model
    if device_type == "mac": # MFlux on macOS
        print("Loading MFlux model...")
        image_model = Flux1(
            model_config=ModelConfig.FLUX1_DEV,
            quantize=8,
            lora_paths=[f"{os.path.abspath(os.path.dirname(__file__))}/fine-tune/models/whatsapp_freemoji.safetensors"],
            lora_scales=[1.0],
        )

        st.session_state.image_model = image_model
        print("MFlux model loaded.")

    else: # Diffusers for CUDA/CPU
        if device == "cuda":
            print("Loading Diffusers model for CUDA...")
            torch_dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
            pipe = FluxPipeline.from_pretrained(
                "black-forest-labs/FLUX.1-dev",
                torch_dtype=torch_dtype,
                use_safetensors=True,
            )

            lora_path = f"{os.path.abspath(os.path.dirname(__file__))}/fine-tune/models/whatsapp_freemoji.safetensors"
            if os.path.exists(lora_path):
                pipe.load_lora_weights(lora_path)

            pipe = pipe.to(device)
            st.session_state.image_model = pipe
            print("Diffusers model loaded.")

        else:
            # Set an error message for CPU users
            st.session_state.model_error = (
                "**Hardware Not Supported:** Image generation requires an NVIDIA GPU (CUDA) or an Apple Silicon Mac. "
                "This machine's CPU is not supported for this model."
            )
            st.session_state.models_loaded = True
            return

    # Load the Language Model
    if device_type == "mac":
        model_name = "mlx-community/Meta-Llama-3.1-8B-Instruct-4bit" 
        
        print(f"Loading MLX model: {model_name}...")
        llm, tokenizer = load(model_name)
        
        st.session_state.llm = llm
        st.session_state.tokenizer = tokenizer
        print("MLX model loaded.")

    else: # Non-Mac
        model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct" 
        
        llm = LLM(
            model=model_name,
            tensor_parallel_size=1,
            gpu_memory_utilization=0.9,
            trust_remote_code=True,
            max_model_len=8192,
        )
        
        st.session_state.llm = llm
        print("VLM model loaded.")

    st.session_state.models_loaded = True

# Streamlit app
def main():
    st.title("Freemoji: Genmoji for Whatsapp!")

    # Load models only once at the start of the session
    if "models_loaded" not in st.session_state:
        with st.spinner("Warming up the engines... Loading models for the first time..."):
            load_models()

    # Display error and stop if models couldn't be loaded
    if "model_error" in st.session_state:
        st.error(st.session_state.model_error)
        return
    
    st.write("Generate images based on your prompts!")

    st.success(f"Detected device: {st.session_state.device_type.title()} on {'Metal' if not st.session_state.device else st.session_state.device.upper()}")

    # Input fields
    user_prompt = st.text_input("Enter your prompt", value="A squirrel holding an iPhone")
    use_prompt_assistant = st.checkbox("Use Prompt Assistant", value=True)
    width = st.number_input("Image Width (px)", min_value=16, max_value=1024, value=160)
    height = st.number_input("Image Height (px)", min_value=16, max_value=1024, value=160)
    upscale_factor = st.slider("Upscale Factor", min_value=1, max_value=10, value=5)
    output_path = st.text_input("Output Path", value="output/freemoji.png")

    # Generate image button
    if st.button("Generate Image"):
        try:
            with st.spinner("Generating... Please wait!"):
                final_prompt = user_prompt
                if use_prompt_assistant:
                    st.info("Prompt Assist is refining your prompt...")
                    final_prompt = update_prompt(
                        user_prompt,
                        st.session_state.device_type,
                        llm=st.session_state.get("llm"),
                        tokenizer=st.session_state.get("tokenizer")
                    )
                    st.write("**Prompt Assist:** " + final_prompt)
                
                st.info("Generating image...")
                image = generate_image(
                    final_prompt, width, height,
                    st.session_state.device_type,
                    model=st.session_state.image_model,
                    device=st.session_state.device
                )

                new_img = image.resize(
                    (width * upscale_factor, height * upscale_factor), Image.LANCZOS
                )

                unique_path = get_unique_path(output_path)
                os.makedirs(os.path.dirname(unique_path), exist_ok=True)
                new_img.save(unique_path)

                st.image(new_img, caption="Generated Image")
                st.success(f"Image saved to {unique_path}")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()