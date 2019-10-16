# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyPostsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 职位名
    positionname = scrapy.Field()

    # 职位链接
    positionlink = scrapy.Field()

    # 职位类别
    postiontype = scrapy.Field()

    # 工作地点
    workposition = scrapy.Field()

    # 工作内容
    responsibility = scrapy.Field()

    # 工作要求
    requirement = scrapy.Field()

    # 发布时间
    publictime = scrapy.Field()

    # 公司
    company = scrapy.Field()

    # 工资
    salary = scrapy.Field()

