# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TextbookSpiderItem(scrapy.Item):
    # 年级
    grade = scrapy.Field()

    # 章节
    chapter = scrapy.Field()

    # 课文来源:0-文本;1-图片;
    source = scrapy.Field()

    # 课文内容
    context = scrapy.Field()

    # url
    url = scrapy.Field()

    # image urls
    image_urls = scrapy.Field()

    # image paths
    image_paths = scrapy.Field()
