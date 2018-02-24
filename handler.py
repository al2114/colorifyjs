from bs4 import BeautifulSoup as Soup
from html.parser import HTMLParser
from PIL import Image
import random
import requests
from io import BytesIO
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json 



def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

def get_links(query_string, num_images):
    #initialize place for links
    links = []
    #step by 100 because each return gives up to 100 links
    for i in range(0,num_images,100):
        url = 'https://www.google.com/search?q='+query_string+'&tbm=isch&source=lnms'
        #&tbm=isch&ved=0ahUKEwjjovnD7sjWAhUGQyYKHTmrC2kQuT0I7gEoAQ&start='+str(i)+'\
        #&yv=2&vet=10ahUKEwjjovnD7sjWAhUGQyYKHTmrC2kQuT0I7gEoAQ.1m7NWePfFYaGmQG51q7IBg.i&ijn=1&asearch=ichunk&async=_id:rg_s,_pms:s'

        #set user agent to avoid 403 error
        request = Request(url, None, {'User-Agent': 'Mozilla/5.0'}) 
        r = urlopen(request)


        #returns json formatted string of the html
        html = urlopen(request).read().decode('utf-8')

        #use BeautifulSoup to parse as html
        soup = Soup(html,'html.parser')

        #all img tags, only returns results of search
        imgs = soup.find_all('img')

        #loop through images and put src in links list
        for j in range(len(imgs)):
            links.append(imgs[j]["src"])

    return links


def get_colour_scheme(query):
    
    urls = get_links(query,3)
    
    response = requests.get(urls[random.randint(0,len(urls)-1)])
    img = BytesIO(response.content)
    
    imgdata = img.read()
    
    
    url = "http://www.pictaculous.com/api/1.0/"
    post_fields = {'image': imgdata}
    
    
    request = Request(url, urlencode(post_fields).encode())
    response = urlopen(request).read().decode()
    
    parsed = json.loads(response) 
    return parsed['info']['colors']












