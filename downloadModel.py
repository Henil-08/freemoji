import json
from huggingface_hub import hf_hub_download

# Read info.json
with open("./info.json", "r") as f:
    models = json.load(f)

# Print model
print(
    f"{models['name']} ({models['model'].split('/')[1]})\n> {models['description']}"
)

# Get user affirmation
choice = input("\Press Y/y to Start Downloading!")

if choice.lower() == "y":
    filename = f"{models['name']}.safetensors"

    print(f"\nDownloading {models['name']}...")
    print(
        "Downloaded weights to: "
        + hf_hub_download(
            repo_id=models["huggingface"], filename=filename, local_dir="./fine-tune/models/"
        )
    )
else:
    print("Invalid selection")