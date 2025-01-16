import glob
from PIL import Image
from io import BytesIO
from pathlib import Path


def create_white_background_image(image_data):
    img = Image.open(BytesIO(image_data))
    if img.mode == "RGBA":
        background = Image.new("RGBA", img.size, "WHITE")
        background.paste(img, mask=img)
        return background
    return img


def setup_folders():
    emoji_dir = Path("emoji")
    raw_dir = Path("raw")
    emoji_dir.mkdir(exist_ok=True)
    raw_dir.mkdir(exist_ok=True)
    return emoji_dir, raw_dir


def get_next_number(emoji_dir):
    existing_files = glob.glob(str(emoji_dir / "img*.png"))
    if not existing_files:
        return 1
    numbers = [int(f.split("img")[-1].split(".")[0]) for f in existing_files]
    return max(numbers) + 1 if numbers else 1