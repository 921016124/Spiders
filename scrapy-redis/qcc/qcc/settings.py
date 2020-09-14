# -*- coding: utf-8 -*-

# Scrapy settings for qcc project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'qcc'

SPIDER_MODULES = ['qcc.spiders']
NEWSPIDER_MODULE = 'qcc.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 2  # 配置执行的最大并发请求数 default:32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3  # 为同一网站的请求配置延迟（单位：秒）
# The download delay setting will honor only one of:  下载延迟设置将只支持以下中的一个
#CONCURRENT_REQUESTS_PER_DOMAIN = 16  # 每个域名同时请求的数量
#CONCURRENT_REQUESTS_PER_IP = 16  # 每个IP同时请求的数量

# Disable cookies (enabled by default)  # 不启用cookies
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:  重写默认的请求头
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares 开放或关闭爬虫中间件
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'qcc.middlewares.QccSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares  开放或关闭下载中间件
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'qcc.middlewares.QccDownloaderMiddleware': 543,
#    'qcc.middlewares.ProxyMiddleware': 100,
# }

# Enable or disable extensions  开放或关闭扩展
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines  配置item管道
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'qcc.pipelines.QccPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)   开放或配置自动限流扩展（单位：s）
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True  # 自动限流开关
# The initial download delay  初始下载延迟
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies  在高延迟情况下设置的最大下载延迟
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to Scrapy each remote server应并行发送到每个远程服务器的平均请求数
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received: 启用为收到的每个响应显示限制状态
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default) 启用和配置HTTP缓存（默认情况下禁用）
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0    # http缓存请求到期秒数
#HTTPCACHE_DIR = 'httpcache'      # htpp缓存存储地址
#HTTPCACHE_IGNORE_HTTP_CODES = [] # http缓存忽略http代码
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'  # http缓存存储 ？

# MongoDB Configuration
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'SunLine'
MONGODB_DOCNAME = 'l_qcc'

#启用scrapy-redis自带的去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
##启用调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#是否在关闭spider的时候保存记录，保存（TRUE）,不保存（False）
SCHEDULER_PERSIST = True
#使用优先级调度请求队列 （默认使用）
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

# Redis Configuration
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_PARAMS = {
    'password': '123456',
}