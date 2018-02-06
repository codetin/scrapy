# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BcyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
    rank = scrapy.Field()
    title = scrapy.Field()
    auth_name = scrapy.Field()
    auth_url = scrapy.Field()
    cartoon_name = scrapy.Field()
    following = scrapy.Field()
    follower = scrapy.Field()
    state = scrapy.Field()
    city = scrapy.Field()

    pass
