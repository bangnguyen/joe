# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JoeItem(scrapy.Item):
    name = scrapy.Field()

    pass

#class Comment(scrapy.Item):
#    link = scrapy.Field()
#    content = scrapy.Field()
#    author = scrapy.Field()
#    date_time = scrapy.Field()
#    thread_name = scrapy.Field()
#    pass