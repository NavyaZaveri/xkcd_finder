from scraper import xkcd_scraper
import requests

'''
init  
'''

APP_ENDPOINT = "localhost:800"


def insert_endpoint():
    return APP_ENDPOINT + "/"


def run(start, end):
    for comic in xkcd_scraper.scrape(0, 20):
        print(comic)


run(0, 20)
