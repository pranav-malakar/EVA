import requests
import json
from PIL import Image
from io import BytesIO

key_Path = "Api_Key\Api_Key.json"
file = open(key_Path)
Api_Key = json.load(file)

def upload_to_imgur(image_path):
    url = "https://api.imgur.com/3/upload"
    headers = {
        "Authorization": Api_Key["Imgur_Authorization"]
    }
    with open(image_path, "rb") as f:
        files = {"image": f}
        response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        data = response.json()
        image_url = data["data"]["link"]
        return image_url
    else:
        print("Failed to upload image to Imgur.")
        return None

if __name__ == "__main__":
    image_path = "path.png"
    image_url = upload_to_imgur(image_path)
    if image_url:
        print("Image uploaded to Imgur:", image_url)
