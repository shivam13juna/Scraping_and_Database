# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item


class GrandItem(Item):
    # Primary Fields
    # Name of Developer
    developer = Field()

    # Size of Area
    area = Field()

    # Total number of bedrooms
    no_bedroom = Field()

    # Total number of bathrooms
    no_bathroom = Field()

    # Status of property
    status = Field()

    # Type of Property
    property_type = Field()

    # If Car Parking Present
    car_parking = Field()

    # If apartment is unfurnished
    furnished_status = Field()


    