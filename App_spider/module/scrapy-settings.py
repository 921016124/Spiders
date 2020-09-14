# -*- coding: utf-8 -*-

# Scrapy settings for Yjt project  
ygt项目的爬虫设置
# For simplicity, this file contains only settings considered important or 
# commonly used. You can find more settings consulting the documentation:
为了简单起见,此文件仅包含被认为重要的设置或常用的。您可以在参考文档中找到更多设置：

#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Yjt'

SPIDER_MODULES = ['Yjt.spiders']
NEWSPIDER_MODULE = 'Yjt.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
通过在用户代理上标识您自己（和您的网站）负责任地爬行
USER_AGENT = '"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",'

# Obey robots.txt rules
遵守robots.txt规则
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
配置Scrapy执行的最大并发请求（默认值：16）
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
为同一网站的请求配置延迟（默认值：0）
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
下载延迟设置仅支持
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
禁用Cookie
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
禁用Telnet控制台（默认启用）
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
重写默认请求头
DEFAULT_REQUEST_HEADERS = {
        "Host": "app.finchina.com",
        "client": "finchina",
        "system": "v4.3.1.551,13.2.3,iOS,iPhone,iPhone,iPhone11,8",
        "Accept-Language": "zh-Hans-CN;q=1.0",
        "Accept-Encoding": "gzip;q=1.0, compress;q=0.5",
        "Connection": "keep-alive",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Referer": "https://app.finchina.com/finchinaAPP/bondDefault/breakContractInfo/dynamics_.html?user=&token=",
        "token": "ee7d9333-95fe-4530-b901-e05b35211cf4",
        "X-Requested-With": "XMLHttpRequest"
}

# Enable or disable spider middlewares
启用或禁用spider中间件
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Yjt.middlewares.YjtSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
启用或禁用下载程序中间件
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'Yjt.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
启用或禁用扩展
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
配置 item 对象管道
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'Yjt.pipelines.YjtPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
