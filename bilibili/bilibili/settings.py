# -*- coding: utf-8 -*-

# Scrapy settings for bilibili project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'bilibili'

SPIDER_MODULES = ['bilibili.spiders']
NEWSPIDER_MODULE = 'bilibili.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bilibili (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 最大并发数
# 注意：并发数太大的时候，retry时会导致很多请求同时retry，然后retry_count 就会很多很多，
# 应当适当的调高retry_count值,和TIMEOUT值，还有count的阈值
CONCURRENT_REQUESTS = 256

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# # 每个domain并发量，设置为超大值，代表不限制
CONCURRENT_REQUESTS_PER_DOMAIN = 1000000
# 单个ip并发量，设置为0，代表不限制
CONCURRENT_REQUESTS_PER_IP = 0

# Disable cookies (enabled by default)
# # 禁用cookies
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'bilibili.middlewares.BilibiliSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {

    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 530,  # 开启retry模块
    # 'bilibili.middlewares.ProxyMiddleware': 542,  // 用flask 得到的代理
    # 'bilibili.middlewares.ProxyMiddleware2': 542, //用hq代理
    'bilibili.middlewares.RestartvpnMiddleware': 542,
    'bilibili.middlewares.UserAgentmiddleware': 543,

}
# DOWNLOAD_DELAY = 0.25
# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}
#
# 重试次数
RETRY_ENABLED = True
RETRY_TIMES = 20

# 下载超时
DOWNLOAD_TIMEOUT = 15

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'bilibili.pipelines.MongoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPERROR_ALLOWED_CODES = [403]
# 抓取的时候会忽略被封的IP 403，ignore_response，这个url
# 等于被忽略掉了，所以要加入403 到 RETRY_HTTP_CODES
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408, 403]
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
MONGO_URI = 'localhost'
MONGO_DB = 'bilivideo'
PROXY_URL = 'http://127.0.0.1:5555/random'
# PROXY_URL = 'http://127.0.0.1:5010/get'
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None  # 无密码为None
# REDIS_PROXY_DB = 10
REDIS_PROXY_DB = 10
