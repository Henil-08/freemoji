import requests
from bs4 import BeautifulSoup
import re
import json

def fetch_and_process_emojis():
    url = 'https://emojigraph.org/whatsapp/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_emoji_data = []

    # Process divs 7 through 15
    for div_num in range(7, 16):
        selector = f'#category__first > div > div > div.col-12.col-lg-8 > div:nth-child({div_num})'
        category_div = soup.select_one(selector)
        
        if category_div:
            # Process images in this div
            for img in category_div.find_all('img'):
                if 'src' in img.attrs:
                    path = img['src']
                    
                    # Extract emoji name
                    name_match = re.search(r'/([^/]+)_[^/]+\.png$', path)
                    if name_match:
                        name = name_match.group(1)
                        
                        # Process URL
                        processed_url = path.replace('/72/', '/')
                        full_url = f"https://emojigraph.org{processed_url}"
                        
                        # Create processed name
                        processed_name = name.replace('-', ' ') + ' emoji'
                        
                        all_emoji_data.append({
                            'link': full_url,
                            'name': name,
                            'processed': processed_name,
                        })
    
    return all_emoji_data

def main():
    emoji_data = fetch_and_process_emojis()
    with open('emojis.json', 'w', encoding='utf-8') as f:
        json.dump(emoji_data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()