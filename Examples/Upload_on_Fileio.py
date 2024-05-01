import requests
import time
import os
from PIL import Image

def upload_to_file_io(image_path):
    url = "https://file.io/"
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files)
    if response.status_code == 200:
        data = response.json()
        file_url = data["link"]
        return file_url
    else:
        print("Failed to upload image to file.io.")
        return None

image_path = "path_1712863986172856.png"
file_url = upload_to_file_io(image_path)
if file_url:
    print("Image uploaded to file.io:", file_url)