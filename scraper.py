import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.http import Request
import csv
import requests

output = open("data.csv", "w", newline='')
writer = csv.writer(output)
writer.writerow(['Link', 'Incorrect Usage(s)', 'Count'])
uniqueLinks = set()
incorrectLinks = set()

#class TribeQuestSpider(scrapy.Spider): #create subclass of Spider class provided by Scrapy
class TribeQuestSpider(CrawlSpider):
    name = "tribequest_spider" #setting name of spider
    allowed_domains = ['wm.edu']
    start_urls = ['https://www.wm.edu/']

    rules = [Rule(LinkExtractor(canonicalize=True, unique=True), follow=True, callback="parse")]

    #Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=False)

    #Method which triggers when the spider finishes recursively parsing
    def closed(self, reason):
        output.close()
        print("# of Unique Links: " + str(len(uniqueLinks)))
        with open('links.txt', 'w') as file:
            for link in sorted(uniqueLinks):
                file.write(link+"\n")

    #Method for parsing links
    def parse(self, response):
        extractor = LinkExtractor(canonicalize=True, unique=True, allow_domains='wm.edu', deny=uniqueLinks)
        links = extractor.extract_links(response)
        print("Unique Links Found: " + str(len(links)))
        for link in links:
            uniqueLinks.add(link.url)
            r = requests.get(link.url)
            incorrectUsages = set()
            incorrectCount = 0
            if "The College of William and Mary".lower() in r.text.lower() or "The College of William & Mary".lower() in r.text.lower() or "College of William and Mary".lower() in r.text.lower() or "College of William & Mary".lower() in r.text.lower():
                if "The College of William and Mary".lower() in r.text.lower():
                    incorrectUsages.add("The College of William and Mary")
                    incorrectCount += r.text.lower().count("The College of William and Mary".lower())
                if "The College of William & Mary".lower() in r.text.lower():
                    incorrectUsages.add("The College of William & Mary")
                    incorrectCount += r.text.lower().count("The College of William and Mary".lower())
                if "College of William and Mary".lower() in r.text.lower():
                    incorrectUsages.add("College of William and Mary")
                    incorrectCount += r.text.lower().count("The College of William and Mary".lower())
                if "College of William & Mary".lower() in r.text.lower():
                    incorrectUsages.add("College of William & Mary")
                    incorrectCount += r.text.lower().count("The College of William and Mary".lower())

                if link.url not in incorrectLinks:
                    incorrectLinks.append(link.url)
                    #Write line to output file with link, incorrect usage(s), and the count of the incorrect usage(s)
                    line = []
                    line.append(link.url)
                    line.append(", ".join([incorrectUsage for incorrectUsage in incorrectUsages]))
                    line.append(str(incorrectCount))
                    writer.writerow(line)
            yield scrapy.Request(link.url, callback=self.parse)

####

# from bs4 import BeautifulSoup
# import urllib.request
# import re

# def add(array, url):
#     if url not in array:
#         array.append(url)
#         getLinks(array, url)
#
# def getLinks(array, url):
#     req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36","X-Requested-With": "XMLHttpRequest"})
#     page = urllib.request.urlopen(req)
#     soup = BeautifulSoup(page, 'html.parser')
#
#     for link in soup.findAll('a'):
#         href = link.get('href')
#         if href is None:
#             continue
#         if href is "#":
#             continue
#         elif href.startswith("/"):
#             href = "https://www.wm.edu/" + href
#             if "wm.edu" in href.lower():
#                 add(array, href)
#         elif href.startswith("https://www.wm.edu"):
#             add(array, href)
#
# links = []
# url = "https://www.wm.edu/"
# getLinks(links, url)
# print("Number of links: " + str(len(links)))
# for link in links:
#     print(link)
