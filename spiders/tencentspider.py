# -*- coding: utf-8 -*-
import scrapy
from scrapy_posts.items import ScrapyPostsItem
import json


class TencentspiderSpider(scrapy.Spider):
    name = 'tencentspider'
    allowed_domains = ['careers.tencent.com']

    url = 'https://careers.tencent.com/tencentcareer/api/post/Query?&pageSize=30&pageIndex='

    detail_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?postId='
    offset = 1
    start_urls = [url + str(offset)]

    def parse(self, response):
        """
        在开始页面
        :param response:
        :return:
        """
        # 获取数据
        data = json.loads(response.text)

        # 获取总数
        count = data['Data']['Count']

        # 算出总页数 一页30
        pagenum = count // 30

        # 获取所有的职业列表
        posts = data['Data']['Posts']

        # 向每个连接发送请求

        for post in posts:
            yield scrapy.Request(self.detail_url + post['PostId'], callback=self.detail_parse)

        # 下载下一页
        if self.offset < pagenum:
            self.offset += 1
            # 重新发送请求,Request(url,callback=回调函数（self.parse）)
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

    def detail_parse(self, response):
        """
        爬取职业详细
        :param response:
        :return:
        """

        # 获取数据
        data = json.loads(response.text)

        item = ScrapyPostsItem()

        # 获取职业名
        item['positionname'] = data['Data']['RecruitPostName']

        # 获取职位连接
        item['positionlink'] = data['Data']['PostURL']

        # 获取发布时间
        item['publictime'] = data['Data']['LastUpdateTime']

        # 工作内容
        item['responsibility'] = data['Data']['Responsibility']

        # 工作要求
        item['requirement'] = data['Data']['Requirement']

        # 职位类别
        item['postiontype'] = data['Data']['CategoryName']

        # 职位地点
        item['workposition'] = data['Data']['LocationName']

        # 公司
        item['company'] = '腾讯'

        # 薪水
        item['salary'] = "#"

        yield item
