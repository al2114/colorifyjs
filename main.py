from handler import *
from PIL import Image, ImageTk
import random
import requests
from io import BytesIO

urls = get_links("pesto",3)

rand = random.randint(0,len(urls))

response = requests.get(urls[rand])
img = Image.open(BytesIO(response.content))

print(img)
