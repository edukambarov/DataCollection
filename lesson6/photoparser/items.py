# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Compose


class PhotoparserItem(scrapy.Item):
    author = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    categories = scrapy.Field()
    img = scrapy.Field(output_processor=TakeFirst())
    post_url = scrapy.Field(output_processor=TakeFirst())

