from PIL import Image
import os
import sys
from utils import get_resized_filename


def resize_image(input_path, scale=5):
    """Resize image by given scale factor using Lanczos resampling"""
    try:
        # Open and resize image
        with Image.open(input_path) as img:
            width, height = img.size
            new_img = img.resize((width * scale, height * scale), Image.LANCZOS)

            # Save resized image
            output_path = get_resized_filename(input_path)
            new_img.save(output_path)
            print(f"Saved resized image to: {output_path}")

    except Exception as e:
        print(f"Error processing image: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python resize_image.py <image_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    resize_image(input_path)