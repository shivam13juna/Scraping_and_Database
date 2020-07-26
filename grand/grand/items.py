# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item


class GrandItem(Item):
    # Primary Fields
    # Title of Product
    title = Field()

    # Total no of ratings
    no_ratings = Field()

    # Rating of product
    rating = Field()

    # Price of product
    price = Field()

    # # Status of property
    # status = Field()

    # # Type of Property
    # property_type = Field()

    # # If Car Parking Present
    # car_parking = Field()

    # # If apartment is unfurnished
    # furnished_status = Field()
