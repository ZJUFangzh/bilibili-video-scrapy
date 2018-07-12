# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class BilibiliSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BilibiliDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


import random  # 随机选择
from .useragent import agents  # 导入前面的
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import logging
import requests
from redis import StrictRedis


class UserAgentmiddleware(UserAgentMiddleware):
    # 随机user agent的中间件
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent

# 用flask做代理的，不使用


class ProxyMiddleware():
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    def get_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def del_proxy(self, proxy):
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

    def check_proxy(self, proxy):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        # print('验证代理：', proxy)
        proxies = {'http': proxy}
        try:
            req = requests.get('https://www.bilibili.com',
                               headers=headers, proxies=proxies, timeout=3)
            return True
        except:
            self.del_proxy(proxy)
            print('删除代理:', proxy)
            return False

        # print('验证代理：', proxy, req.status_code)

    def process_request(self, request, spider):
        # print('treretime', request.meta.get('retry_times'))
        # if request.meta.get('retry_times'):
        proxy = self.get_proxy()
        if proxy:
            uri = 'https://{}'.format(proxy)
            self.logger.debug('using proxy:' + proxy)
            request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        s = cls(proxy_url=settings.get('PROXY_URL'))
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(s.spider_error, signal=signals.spider_error)
        # s.proxy_url = settings.get('PROXY_URL')

        return s

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('爬虫开启: %s' % spider.name)

    def spider_closed(self, spider):
        spider.logger.info('爬虫关闭: %s' % spider.name)

    def spider_error(self, failure, response, spider):
        # 增加记录爬虫报错的函数，连接spider_error信号
        spider.logger.error('[%s],错误:%s' %
                            (response.url, failure.getTraceback()))
        with open("./error_spider.txt", "a") as fa:
            fa.write(response.url)
            fa.write("\n")
        with open("./error_spider_info.txt", "a") as fb:
            fb.write("Error on {0}, traceback: {1}".format(
                response.url, failure.getTraceback()))
            fb.write("\n")


from scrapy.conf import settings

# 用redis直接拿代理的，不使用


class ProxyMiddleware2():

        # print('验证代理：', proxy, req.status_code)

    def process_request(self, request, spider):
        # 使用代理ip池的中间件
        # 配合https://github.com/arthurmmm/hq-proxies使用
        # 若使用请在settings中开启

        proxy = self.redis_db.srandmember("hq-proxies:proxy_pool", 1)

        if proxy:
            proxy = proxy[0].decode()
            spider.logger.info('使用代理[%s]访问[%s]' % (proxy, request.url))

            request.meta['proxy'] = proxy
        else:
            spider.logger.warning('不使用代理访问[%s]' % request.url)
        return None

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(s.spider_error, signal=signals.spider_error)
        # s.proxy_url = settings.get('PROXY_URL')

        return s

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('爬虫开启: %s' % spider.name)
        self.redis_db = StrictRedis(
            host=settings["REDIS_HOST"],
            port=settings["REDIS_PORT"],
            password=settings["REDIS_PASSWORD"],
            db=settings["REDIS_PROXY_DB"],
        )

    def spider_closed(self, spider):
        spider.logger.info('爬虫关闭: %s' % spider.name)

    def spider_error(self, failure, response, spider):
        # 增加记录爬虫报错的函数，连接spider_error信号
        spider.logger.error('[%s],错误:%s' %
                            (response.url, failure.getTraceback()))
        with open("./error_spider.txt", "a") as fa:
            fa.write(response.url)
            fa.write("\n")
        with open("./error_spider_info.txt", "a") as fb:
            fb.write("Error on {0}, traceback: {1}".format(
                response.url, failure.getTraceback()))
            fb.write("\n")


import os
import time

# 使用VPN不断的重拨，来更换IP


class RestartvpnMiddleware():

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(s.spider_error, signal=signals.spider_error)

        return s

    def restart(self):

        os.system('rasdial /disconnect')
        os.system('rasdial vpncon 21725033 052533')
        time.sleep(1)

    def process_request(self, request, spider):
        # 先知道retry的次数
        retry_times = request.meta.get('retry_times')
        if not retry_times:
            self.retry_count = 0
        # 超过2次数很多次的话，应该就可以判断这个时候断网了，重新连接VPN
        if retry_times != None and retry_times >= 2:
            self.retry_count += 1
            if self.retry_count > 100:
                self.restart()
                self.retry_count = -300

    def process_response(self, request, response, spider):
        # retry_times = request.meta.get('retry_times')
        # print('retry_times', retry_times)
        # 如果出现状态码异常，很多次就代表被封了IP，重启一下VPN更换IP
        # print(response.status)
        if response.status != 200:
            self.count += 1
        else:
            self.count = 0
        if self.count > 40:
            self.restart()
            self.count = -300
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('爬虫开启: %s' % spider.name)
        self.count = 0
        self.retry_count = 0

    def spider_closed(self, spider):
        spider.logger.info('爬虫关闭: %s' % spider.name)

    def spider_error(self, failure, response, spider):
        # 增加记录爬虫报错的函数，连接spider_error信号
        spider.logger.error('[%s],错误:%s' %
                            (response.url, failure.getTraceback()))
        with open("./error_spider.txt", "a") as fa:
            fa.write(response.url)
            fa.write("\n")
        with open("./error_spider_info.txt", "a") as fb:
            fb.write("Error on {0}, traceback: {1}".format(
                response.url, failure.getTraceback()))
            fb.write("\n")
