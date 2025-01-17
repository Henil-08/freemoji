import streamlit as st # type: ignore
from promptAssist import update_prompt
from generate import generate_image
from PIL import Image # type: ignore
from utils import get_unique_path
import os

# Streamlit app
def main():
    st.title("Freemoji: Genmoji for Whatsapp!")
    st.write("Generate images based on your prompts!")

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
            with st.spinner("Generating your image... Please wait!"):
                # Handle prompt assistant logic
                if use_prompt_assistant:
                    prompt_response = update_prompt(user_prompt)
                    st.write("Prompt Created by Assistant: " + prompt_response)
                else:
                    prompt_response = user_prompt
                    st.write("Using Original Prompt: " + prompt_response)

                # Generate the image
                image = generate_image(prompt_response, width, height)

                # Upscale the image
                output_width, output_height = image.size
                new_img = image.resize(
                    (output_width * upscale_factor, output_height * upscale_factor), Image.LANCZOS
                )

                # Save the image
                output_path = get_unique_path(output_path)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                new_img.save(output_path)

                # Display the image
                st.image(new_img, caption="Generated Image", use_container_width=True)
                st.success(f"Image saved to {output_path}")

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()