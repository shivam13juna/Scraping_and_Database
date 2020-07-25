import scrapy
from grand.items import GrandItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from scrapy.http import Request
import time
import random
from urllib.parse import urljoin

headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
 'accept-language': 'en-US,en;q=0.9',
 'cache-control': 'max-age=0',
 'cookie': 'prov=6ee1b1c0-a975-57c1-b806-d6f02acdc078; _ga=GA1.2.1770530859.1579667732; __qca=P0-709205387-1579667731930; __gads=ID=7abeba23853bfab5:T=1579667732:S=ALNI_MZQpLsyZugJqQyXRBUJPOkgNjsDbw; sgt=id=57291405-92ae-4989-a741-f989cf2c6903; _gid=GA1.2.1065622312.1595226703; arp_scroll_position=136; acct=t=JE1j0YL6mlLl7%2bJDAZ0zaTJQ%2bUidPKXE&s=xcKiH08vYJFwXKLlol2HcBhRPB70gUZR',
 'dnt': '1',
 'referer': 'https://www.google.com/',
 'sec-fetch-dest': 'document',
 'sec-fetch-mode': 'navigate',
 'sec-fetch-site': 'cross-site',
 'sec-fetch-user': '?1',
 'upgrade-insecure-requests': '1',
 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}


class BasicSpider(scrapy.Spider):
    name = 'manual'
    allowed_domains = ['amazon']
    start_urls = ['https://www.amazon.in/s?k=bicycle&ref=nb_sb_noss']#,
                #   'https://www.magicbricks.com/propertyDetails/2-BHK-1404-Sq-ft-Multistorey-Apartment-FOR-Sale-Electronic-City-Phase-2-in-Bangalore&id=4d423439383237313532']

    def parse_item(self, response):
        next_selector = response.xpath('//*[@class="a-normal"]//@href')
        for url in next_selector.extract():
            time.sleep(random.uniform(0, 2))
            yield Request(urljoin(response.url, url), headers = headers)
        # Get item URLs and yield Requests
        item_selector = response.xpath('//a[@class="a-link-normal a-text-normal"]/@href')
        for url in item_selector.extract():
            time.sleep(random.uniform(0, 2))
            yield Request(urljoin(response.url, url), headers = headers, callback=self.parse_item)