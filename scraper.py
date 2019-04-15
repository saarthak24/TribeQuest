#import scrapy

#class TribeQuestSpider(scrapy.Spider): #create subclass of Spider class provided by Scrapy
#    name = "tribequest_spider" #setting name of spider
#    start_urls = ['https://www.wm.edu/']

from bs4 import BeautifulSoup
import urllib.request
import re

def add(array, url):
    if url not in array:
        array.append(url)
        getLinks(array, url)

def getLinks(array, url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36","X-Requested-With": "XMLHttpRequest"})
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

    for link in soup.findAll('a'):
        href = link.get('href')
        if href is None:
            continue
        if href is "#":
            continue
        elif href.startswith("/"):
            href = "https://www.wm.edu/" + href
            if "wm.edu" in href.lower():
                add(array, href)
        elif href.startswith("https://www.wm.edu"):
            add(array, href)

links = []
url = "https://www.wm.edu/"
getLinks(links, url)
print(links)
