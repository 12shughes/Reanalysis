import os
import requests
from bs4 import BeautifulSoup
import fnmatch
import urllib.request

# Directory where you want to save the files
save_dir = '/disco/share/sh1293/EMARS_data/Background/Raw/'

# Ensure the save directory exists
os.makedirs(save_dir, exist_ok=True)

# Base URL of the data page
base_url = 'https://www.datacommons.psu.edu'

# URL of the specific data page
url = f'{base_url}/download/meteorology/greybush/emars-1p0/data/'

# Send a request to the page
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Pattern for the .nc files
file_pattern = '/download/meteorology/greybush/emars-1p0/data/emars_v1.0_back_mean_MY29_Ls*.nc'

# Find and download all .nc files
for link in soup.find_all('a'):
    href = link.get('href')
    
    # Check if the href matches the file pattern
    if href and fnmatch.fnmatch(href, file_pattern):
        file_url = f"{base_url}{href}"  # Construct the full file URL
        file_name = os.path.basename(href)
        file_path = os.path.join(save_dir, file_name)
        
        print(f"Downloading {file_url} to {file_path}")
        
        # Download the file using requests and save it to the specified directory
        urllib.request.urlretrieve(file_url, file_path)

print("All files downloaded successfully.")
