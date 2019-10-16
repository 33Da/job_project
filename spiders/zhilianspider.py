# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_posts.items import ScrapyPostsItem


class ZhilianspiderSpider(scrapy.Spider):
    name = 'zhilianspider'
    allowed_domains = ['fe-api.zhaopin.com']

    # cityId = 763 广州   765 深圳  769 江门
    citys = ['763', '765', '769']
    cityId = 0

    offset = 0

    url = 'https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId={0}&start={1}'.format(citys[0], offset)

    start_urls = [url]

    def new_url(self):
        """构造url"""
        return 'https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId={0}&start={1}'.format(self.citys[self.cityId], self.offset)

    def parse(self, response):
        # 获取数据
        data = json.loads(response.text)

        posts = data['data']['results']

        item = ScrapyPostsItem()

        for post in posts:
            # 获取职业名
            item['positionname'] = post['jobName']

            # 获取职位连接
            item['positionlink'] = post['positionURL']

            # 获取发布时间
            item['publictime'] = post['updateDate']

            # 工作内容
            item['responsibility'] = post['jobType']['items']

            # 工作要求
            item['requirement'] = post['eduLevel']['name']

            # 职位类别
            item['postiontype'] = post['emplType']
            # 职位地点
            item['workposition'] = post['city']['display']

            # 公司
            item['company'] = post['company']['name']

            # 薪水
            item['salary'] = post['salary']

            yield item

        # 下载下一页
        if self.offset < 1000:
            self.offset += 90
            # 重新发送请求,Request(url,callback=回调函数（self.parse）)
            url = self.new_url()
            yield scrapy.Request(url, callback=self.parse)
        else:
            if self.cityId < len(self.citys):
                self.cityId += 1
                self.offset = 0
                url = self.new_url()
                yield scrapy.Request(url, callback=self.parse)
