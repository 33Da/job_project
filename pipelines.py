# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class ScrapyPostsPipeline(object):
    def __init__(self):
        # 获取setting主机名、端口号和数据库名
        host = '127.0.0.1'
        port = 27017
        dbname = 'myposts'

        # pymongo.MongoClient(host, port) 创建MongoDB链接
        client = pymongo.MongoClient(host=host, port=port)

        # 指向指定的数据库
        mdb = client[dbname]
        # 获取数据库里存放数据的表名
        self.post = mdb['posts']

    def process_item(self, item, spider):
        data = dict(item)

        # 向指定的表里添加数据
        self.post.insert(data)
        return item

