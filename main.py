from handler import *
from PIL import Image
import random
import requests
from io import BytesIO
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json 

urls = get_links("pesto",3)


response = requests.get(urls[random.randint(0,len(urls)-1)])
img = BytesIO(response.content)

imgdata = img.read()


url = "http://www.pictaculous.com/api/1.0/"
post_fields = {'image': imgdata}


request = Request(url, urlencode(post_fields).encode())
response = urlopen(request).read().decode()

parsed = json.loads(response) 
print(parsed['info']['colors'])
