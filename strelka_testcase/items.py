# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    hotel = scrapy.Field()
    type = scrapy.Field()
    legal_entity_name = scrapy.Field()
    region = scrapy.Field()
    inn = scrapy.Field()
    ogrn = scrapy.Field()
    address = scrapy.Field()
    phone_number = scrapy.Field()
    email = scrapy.Field()
    site_url = scrapy.Field()
    classification = scrapy.Field()

    pass