import json
import requests
from utility import setup_folders, get_next_number, create_white_background_image


def download_emojis():
    emoji_dir, raw_dir = setup_folders()
    start_num = get_next_number(emoji_dir)

    with open("emojis/emojisFiltered.json", "r") as f:
        emoji_data = json.load(f)

    total = len(emoji_data)

    for i, emoji in enumerate(emoji_data[start_num - 1 :], start=start_num):
        print(f"Downloading {i}/{total}: {emoji['processed']}")

        response = requests.get(emoji["link"])
        if response.status_code == 200:
            # Save raw version
            raw_path = raw_dir / f"{emoji['name']}.png"
            with open(raw_path, "wb") as f:
                f.write(response.content)

            # Process and save white background version
            img_with_background = create_white_background_image(response.content)
            img_with_background.save(emoji_dir / f"img{i}.png", "PNG")

            # Save text
            with open(emoji_dir / f"img{i}.txt", "w") as f:
                f.write(emoji["processed"])
        else:
            raise Exception(
                f"Failed to download {emoji['processed']}: Status {response.status_code}"
            )


if __name__ == "__main__":
    download_emojis()