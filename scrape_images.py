import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse


url = 'insert url here'

headers = ''

r = requests.get(url=url)

if r.status_code == 200:
    print("Successfully retrieved the webpage")
else:
    print("Failed to retrieve the webpage")

soup = BeautifulSoup(r.content, 'html.parser')

image_tags = soup.find_all('img')

urls = [img['src'] for img in image_tags if 'src' in img.attrs]

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

image_urls = [urljoin(url, img_url) for img_url in urls]
valid_image_urls = [img_url for img_url in image_urls if is_valid_url(img_url)]

os.makedirs('images', exist_ok=True)

for img_url in valid_image_urls:
    try:
        img_data = requests.get(img_url).content
        img_name = os.path.join('images', os.path.basename(urlparse(img_url).path))
        with open(img_name, 'wb') as img_file:
            img_file.write(img_data)
        print(f"Downloaded {img_url}")
    except Exception as e:
        print(f"Could not download {img_url}. Error: {e}")

