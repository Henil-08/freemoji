import torch
from mflux import Config

def generate_image_mflux(model, prompt: str, width: int, height: int):
    """Generate image using a pre-loaded MFlux model."""
    # Generate an image
    image = model.generate_image(
        seed=7,
        prompt=prompt,
        config=Config(
            num_inference_steps=20,
            height=height,
            width=width,
        ),
    )
    return image.image

def generate_image_diffusers(model, prompt: str, width: int, height: int, device: str):
    """Generate image using a pre-loaded Diffusers pipeline."""
    image = model(
        prompt=prompt,
        height=height,
        width=width,
        num_inference_steps=20,
        guidance_scale=0.0,
        generator=torch.Generator(device=device).manual_seed(7),
    ).images[0]
    return image


def generate_image(prompt: str, width: int, height: int, device_type: str, model, device: str = None):
    """Main function to generate image with a pre-loaded model."""
    print(f"Generating with {device_type} backend...")
    if device_type == "mac":
        return generate_image_mflux(model, prompt, width, height)
    elif device == "win/linux":
        return generate_image_diffusers(model, prompt, width, height, device)
    else:
        raise ValueError(f"Unsupported configuration for image generation: {device_type}, {device}")
