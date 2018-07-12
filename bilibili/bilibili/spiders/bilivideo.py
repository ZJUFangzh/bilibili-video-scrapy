# -*- coding: utf-8 -*-
import scrapy

from bilibili.items import BilibiliItem
#
import json
import re


class BilivideoSpider(scrapy.Spider):
    name = 'bilivideo'
    allowed_domains = ['bilibili.com']

# 选择b站从0开始到2500W的视频里面的API，先拿到API里面的参数，再根据ID到具体视频页面中获取参数
    def start_requests(self):
        for i in range(1059717, 26000000):
            url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid=' + \
                str(i)
            yield scrapy.Request(url)

    def parse(self, response):
        # print(response.url)
        js = json.loads(response.body)
        # 判断code是否为0，如果不为0 就是不可以抓取或者不存在的视频
        if js['code'] == 0:
            data = js['data']
            if isinstance(data['view'], int) and data['view'] >= 1000:
                item = BilibiliItem()
                # 将data中的数据都传入item中，并向下继续请求第二级的链接，补全item
                for key in data.keys():
                    item[key] = data[key]
                # yield item
                yield scrapy.Request('https://www.bilibili.com/video/av{}'.format(data['aid']), meta={'item': item}, callback=self.parse_detail)

    def parse_detail(self, response):
        text = response.text
        # print(text)
        # 用正则拿到所有需要的信息
        pattern = re.compile(
            'uploadDate.*?content="(.*?)".*?tname":"(.*?)".*?title":"(.*?)".*?desc":"(.*?)".*?upData.*?mid":"(.*?)","name":"(.*?)".*?sex":"(.*?)".*?fans":(.*?),.*?attention":(.*?),"sign', re.S)
        data = re.search(pattern, text)
        item = response.meta['item']
        item['uploadDate'] = data.group(1)
        item['tname'] = data.group(2)
        item['title'] = data.group(3)
        item['desc'] = data.group(4)
        item['mid'] = data.group(5)
        item['upname'] = data.group(6)
        item['sex'] = data.group(7)
        item['fans'] = data.group(8)
        item['attention'] = data.group(9)
        yield item
