import os
import requests
from bs4 import BeautifulSoup

# Directory where you want to save the files
save_dir = '/disco/share/sh1293/MACDA2_data/Raw/'

# Ensure the save directory exists
os.makedirs(save_dir, exist_ok=True)

# URL of the Zenodo page
url = 'https://zenodo.org/record/5517308'

# Send a request to the page
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find and download all .nc files
for link in soup.find_all('a'):
    href = link.get('href')
    if href and 'files/' in href and href.endswith('.nc?download=1'):
        file_url = f"https://zenodo.org{href}"
        file_name = os.path.basename(href.split('?')[0])
        file_path = os.path.join(save_dir, file_name)
        print(f"Downloading {file_url} to {file_path}")
        
        # Download the file using requests and save it to the specified directory
        file_response = requests.get(file_url)
        with open(file_path, 'wb') as file:
            file.write(file_response.content)

print("All files downloaded successfully.")
