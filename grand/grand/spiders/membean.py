import scrapy
from grand.items import GrandItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from scrapy.http import Request
import time
import random
from urllib.parse import urljoin

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}


class BasicSpider(scrapy.Spider):
    name = 'manual'
    allowed_domains = ['amazon.in']
    start_urls = ['https://www.amazon.in/s?k=bicycle']#,
                #   'https://www.magicbricks.com/propertyDetails/2-BHK-1404-Sq-ft-Multistorey-Apartment-FOR-Sale-Electronic-City-Phase-2-in-Bangalore&id=4d423439383237313532']

    def parse(self, response):
        next_selector = response.xpath('//*[@class="a-normal"]//@href')
        for url in next_selector.extract():
            time.sleep(random.uniform(0, 2))
            print("Next Selector", urljoin(response.url, url))
            yield Request(urljoin(response.url, url), headers = headers)
        # Get item URLs and yield Requests
        item_selector = response.xpath('//a[@class="a-link-normal a-text-normal"]/@href')
        for url in item_selector.extract():
            time.sleep(random.uniform(0, 2))
            print("Item Selector", urljoin(response.url, url))
            yield Request(urljoin(response.url, url), headers = headers, callback=self.parse_item)
    
    def parse_item(self, response):

        """ This is a contract for checking validity of spider

        @url  https://www.amazon.in/s?k=bicycle&ref=nb_sb_noss
        @returns items 1
        @scrapes title no_reviews rating price
        """
        # Create the loader using the response
        iloader = ItemLoader(item=GrandItem(), response=response)


        self.log("title: %s" % response.xpath('//span[@id="productTitle"]/text()').extract()[0].strip())
        self.log("no_reviews: %s" % response.xpath('//span[@id="acrCustomerReviewText"]//text()').extract()[0])
        self.log("rating: %s" % response.xpath('//span[@data-hook="rating-out-of-text"]//text()').extract()[0])
        self.log("price: %s" % response.xpath('//span[@id="priceblock_dealprice"]//text()').extract()[0].strip().replace(u'\xa0', u' '))
        


        iloader.add_xpath("title", '//span[@id="productTitle"]/text()', MapCompose(str.strip))
        iloader.add_xpath("no_ratings", '//span[@id="acrCustomerReviewText"]//text()')
        iloader.add_xpath("rating", '//span[@data-hook="rating-out-of-text"]//text()')
        iloader.add_xpath("price", '//span[@id="priceblock_dealprice"]//text()', lambda x: x[0].strip().replace(u'\xa0', u' '))

        return iloader.load_item()
        # title = response.xpath('//span[@id="productTitle"]/text()').extract()[0].strip()

        # no_reviews = response.xpath('//span[@id="acrCustomerReviewText"]//text()').extract()[0]

        # rating = response.xpath('//span[@data-hook="rating-out-of-text"]//text()').extract()[0]

        # price = response.xpath('//span[@id="priceblock_dealprice"]//text()').extract()[0].strip().replace(u'\xa0', u' ')

    

    # def parse(self, response):
    #     # Get the next index URLs and yield Requests
    #     next_selector = response.xpath('//*[contains(@class,"next")]//@href')
    #     for url in next_selector.extract():
    #         yield Request(urlparse.urljoin(response.url, url))

    #     # Get item URLs and yield Requests
    #     item_selector = response.xpath('//*[@itemprop="url"]/@href')
    #     for url in item_selector.extract():
    #         yield Request(urlparse.urljoin(response.url, url),
    #                       callback=self.parse_item)

    # def parse_item(self, response):
    #     """ This function parses a property page.

    #     @url http://web:9312/properties/property_000000.html
    #     @returns items 1
    #     @scrapes title price description address image_urls
    #     @scrapes url project spider server date
    #     """

    #     # Create the loader using the response
    #     l = ItemLoader(item=PropertiesItem(), response=response)

    #     # Load fields using XPath expressions
    #     l.add_xpath('title', '//*[@itemprop="name"][1]/text()',
    #                 MapCompose(unicode.strip, unicode.title))
    #     l.add_xpath('price', './/*[@itemprop="price"][1]/text()',
    #                 MapCompose(lambda i: i.replace(',', ''), float),
    #                 re='[,.0-9]+')
    #     l.add_xpath('description', '//*[@itemprop="description"][1]/text()',
    #                 MapCompose(unicode.strip), Join())
    #     l.add_xpath('address',
    #                 '//*[@itemtype="http://schema.org/Place"][1]/text()',
    #                 MapCompose(unicode.strip))
    #     l.add_xpath('image_urls', '//*[@itemprop="image"][1]/@src',
    #                 MapCompose(lambda i: urlparse.urljoin(response.url, i)))

    #     # Housekeeping fields
    #     l.add_value('url', response.url)
    #     l.add_value('project', self.settings.get('BOT_NAME'))
    #     l.add_value('spider', self.name)
    #     l.add_value('server', socket.gethostname())
    #     l.add_value('date', datetime.datetime.now())

    #     return l.load_item()