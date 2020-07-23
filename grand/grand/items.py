# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item


class GrandItem(Item):
    # Primary Fields
    title = Field()
    price = Field()
    description = Field()
    address = Field()
    image_urls = Field()

    # Fields to be Calculated
    images = Field()
    