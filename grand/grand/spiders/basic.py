import scrapy
from grand.items import GrandItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['web']
    start_urls = ['https://www.magicbricks.com/propertyDetails/2-BHK-1030-Sq-ft-Multistorey-Apartment-FOR-Sale-Thanisandra-Main-Road-in-Bangalore&id=4d423231313036303433?sem=Y']#,
                #   'https://www.magicbricks.com/propertyDetails/2-BHK-1404-Sq-ft-Multistorey-Apartment-FOR-Sale-Electronic-City-Phase-2-in-Bangalore&id=4d423439383237313532']

    def parse(self, response):
        ''' This function parses properties of a page

        @url https://www.magicbricks.com/propertyDetails/2-BHK-1030-Sq-ft-Multistorey-Apartment-FOR-Sale-Thanisandra-Main-Road-in-Bangalore&id=4d423231313036303433?sem=Y

        @returns items 1 16
        @returns requests 0 
        @scrapes developer area no_bedroom no_bathroom status property_type car_parking furnished_status
        '''



        # item = GrandItem()
        iloader = ItemLoader(item=GrandItem(), response=response)


        self.log("developer: %s" % response.xpath('((//*[@id="thirdFoldDisplay"]//*[@target="_blank"])//text())[1]').extract()[0].strip())
        self.log("area: %s" % response.xpath('//*[@id="coveredAreaDisplay"]//text()').extract()[0] + ' sqft')
        self.log("no_bedroom: %s" % int(''.join(x.strip() for x in response.xpath('//*[@class="seeBedRoomDimen"]//text()').extract())))
        self.log("no_bathroom: %s" % int(response.xpath('//div[contains(@class, "p_infoColumn") and contains(.//div, "Bathrooms")]/*[@class="p_value"]/text()').extract()[0]))
        self.log("status: %s" % response.xpath('//div[contains(@class, "p_infoColumn") and contains(.//div, "Status")]/*[@class="p_value"]/text()').extract()[0])
        self.log("property_type: %s" % response.xpath('//div[contains(@class, "p_infoColumn") and contains(.//div, "Transaction type")]/*[@class="p_value"]/text()').extract()[0])
        self.log("car_parking: %s" % response.xpath('//div[contains(@class, "p_infoColumn") and contains(.//div, "Car parking")]/*[@class="p_value"]/text()').extract()[0])
        self.log("furnished_status: %s" % response.xpath('//div[contains(@class, "p_infoColumn") and contains(.//div, "Furnished status")]/*[@class="p_value"]/text()').extract()[0])

        iloader.add_xpath("developer", '((//*[@id="thirdFoldDisplay"]//*[@target="_blank"])//text())[1]', MapCompose(str.strip))
        iloader.add_xpath("area", '//*[@id="coveredAreaDisplay"]//text()', MapCompose(lambda i: i + ' sqft'))
        iloader.add_xpath("no_bedroom", '//*[@class="seeBedRoomDimen"]//text()', lambda x: ''.join(i.strip() for i in x))
        iloader.add_xpath("no_bathroom", '//div[contains(@class, "p_infoColumn") and contains(.//div, "Bathrooms")]/*[@class="p_value"]/text()', MapCompose(int))
        iloader.add_xpath("status", '//div[contains(@class, "p_infoColumn") and contains(.//div, "Status")]/*[@class="p_value"]/text()')
        iloader.add_xpath("property_type", '//div[contains(@class, "p_infoColumn") and contains(.//div, "Transaction type")]/*[@class="p_value"]/text()')
        iloader.add_xpath("car_parking", '//div[contains(@class, "p_infoColumn") and contains(.//div, "Car parking")]/*[@class="p_value"]/text()')
        iloader.add_xpath("furnished_status", '//div[contains(@class, "p_infoColumn") and contains(.//div, "Furnished status")]/*[@class="p_value"]/text()')

        # We could have also usd iloader.add_value('url', response.url)

        return iloader.load_item()
        