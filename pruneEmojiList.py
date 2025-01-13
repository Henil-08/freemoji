import json

def process_emojis():
    # Read original JSON
    with open('emojis.json', 'r') as f:
        emoji_data = json.load(f)
    
    # Filter out any emoji containing "skin-tone" in name
    filtered_emojis = [
        emoji for emoji in emoji_data 
        if 'skin-tone' not in emoji['name']
    ]
    
    # Write filtered data
    with open('emojisPruned.json', 'w') as f:
        json.dump(filtered_emojis, f, indent=2)

if __name__ == '__main__':
    process_emojis()