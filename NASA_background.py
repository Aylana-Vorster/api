import ctypes
import os
import yaml
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from drawing import draw_text

# Assuming config.yaml is in the same directory as NASA.py
config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

with open(config_path, 'r') as config_file:
    config = yaml.safe_load(config_file)

# Check if config is loaded successfully
if config is not None and 'NASA_token' in config:
    api_key = config['NASA_token']

    try:
        # Fetch APOD data and HD image URL using requests (non-asynchronous)
        response = requests.get("https://api.nasa.gov/planetary/apod?api_key=" + api_key)
        data = response.json()
        hd_url = data["hdurl"]

        # Download the HD image
        pic_response = requests.get(hd_url, stream=True)
        img = Image.open(BytesIO(pic_response.content))

        # Determine the aspect ratio of the original image
        original_aspect_ratio = img.width / img.height

        # Set the desired desktop size
        desktop_size = (1920, 1080)
        desktop_aspect_ratio = desktop_size[0] / desktop_size[1]

        # Crop the image so we may write on the HD version ofthe picture
        if original_aspect_ratio > desktop_aspect_ratio:
            # Crop the width to match the desktop aspect ratio
            new_width = int(desktop_size[0] * (img.height / desktop_size[1]))
            img = img.crop(((img.width - new_width) // 2, 0, (img.width + new_width) // 2, img.height))
        else:
            # Crop the height to match the desktop aspect ratio
            new_height = int(desktop_size[1] * (img.width / desktop_size[0]))
            img = img.crop((0, (img.height - new_height) // 2, img.width, (img.height + new_height) // 2))

        # Resize the cropped image to the desired desktop size
        img = img.resize(desktop_size)

        # Create a drawing object out of the resized and cropped image
        draw = ImageDraw.Draw(img)

        # Decide some attributes around the text
        text_position = (10, 10)
        font_size = 15
        font = ImageFont.truetype("arial.ttf", font_size)

        # Draw text on the image
        draw_text(draw, data["explanation"], text_position, font, img.size[0] - 20, img.size[1] - 20)

        # Save the resized and cropped image in JPEG format with compression
        img_path = os.path.join(os.path.dirname(__file__), f"{data['date']}.jpg")
        img.save(img_path, quality=85)  # Adjust quality as needed

        # Set the desktop background
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, img_path, 3)
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong:",err)
else:
    print("Error loading NASA API key from config.yaml")
