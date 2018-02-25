from bs4 import BeautifulSoup as Soup
from html.parser import HTMLParser
from PIL import Image
import random
import requests
from io import BytesIO
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

def colour_scheme_service(event, context):
    badResponse = {
        "statusCode": 400,
        "body": "Bad request, missing parameter 'url' in query"
    }
    if not 'queryStringParameters' in event:
        return badResponse

    params = event['queryStringParameters']
    if not 'url' in params:
        return badReponse

    url = event['queryStringParameters']['url']

    body = {
        "colors": get_colour_scheme_from_url(url),
        "url": url
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

def image_finder_service(event, context):
    badResponse = {
        "statusCode": 400,
        "body": "Bad request, missing parameter 'keyword' in query string"
    }
    if not 'queryStringParameters' in event:
        return badResponse

    params = event['queryStringParameters']
    if not 'keyword' in params:
        return badReponse

    keyword = event['queryStringParameters']['keyword']

    body = {
        "urls": get_links(keyword),
        "query": keyword
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



def get_links(query_string):
    #initialize place for links
    links = []
    #step by 100 because each return gives up to 100 links
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


def get_colour_scheme_from_url(imgurl):

    print("Getting image")

    response = requests.get(imgurl)
    img = BytesIO(response.content)

    imgdata = img.read()

    print("Passing into pictaculous")

    url = "http://www.pictaculous.com/api/1.0/"
    post_fields = {'image': imgdata}


    request = Request(url, urlencode(post_fields).encode())
    response = urlopen(request).read().decode()

    parsed = json.loads(response)
    return parsed['info']['colors']


def get_colour_scheme(query):

    urls = get_links(query)

    response = requests.get(urls[random.randint(0,len(urls)-1)])
    img = BytesIO(response.content)

    imgdata = img.read()


    url = "http://www.pictaculous.com/api/1.0/"
    post_fields = {'image': imgdata}


    request = Request(url, urlencode(post_fields).encode())
    response = urlopen(request).read().decode()

    parsed = json.loads(response)
    return parsed['info']['colors']

if __name__ == "__main__":
    #hello('','')
#    resp = image_finder_service({'queryStringParameters': { 'keyword': "pesto" }},"")
    resp = colour_scheme_service({'queryStringParameters': { 'url': "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQXSfIu-D2cOWqUQl8nV5Y5YpAeDC_KQc7PMCHI-bjf7gt667pxv3JYmQ" }},"")
    print(resp)

