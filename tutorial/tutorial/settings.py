# Scrapy settings for tutorial project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'tutorial'  # 程序名

SPIDER_MODULES = ['tutorial.spiders']  # 爬虫模块列表
NEWSPIDER_MODULE = 'tutorial.spiders'  # 爬虫模块名


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tutorial (+http://www.yourdomain.com)'
# 用户头
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36 Edg/87.0.664.4"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False  # 是否遵守robots

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32  # 并发请求，默认为32个

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16  # 每个域内最多并发请求
#CONCURRENT_REQUESTS_PER_IP = 16  # 每个IP最多并发请求

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False  # 是否禁止cookies，默认开启

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {  # 默认请求头
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares  # 开启爬虫中间件
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'tutorial.middlewares.TutorialSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares  # 开启下载中间件
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'tutorial.middlewares.TutorialDownloaderMiddleware': 543,
#}


# Enable or disable extensions  # 扩展相关
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines  # 实体对象处理管道
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'tutorial.pipelines.TutorialPipeline': 300,
#}



# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 自定义新的导出数据格式
# FEED_EXPORTERS = {
# 	'excel':'example.my_exporters.ExcelItemExporter',
# }

DOWNLOAD_DELAY=2  # 固定延时2秒
# RANDOMIZE_DOWNLOAD_DELAY=True  # 随机的延迟时间

# 下载中间件
DOWNLOADER_MIDDLEWARES = {
    # 置于HttpProxyMiddleware(750)之前
    # 'tutorial.middlewares.RandomHttpProxyMiddleware':745,
    # 'tutorial.middlewares.ProxyMiddleware':745,  # 随机代理中间件
    "tutorial.middlewares.RandomUserAgentMiddleware": 380,  # 随机UA中间件
}

# 激活管道
ITEM_PIPELINES = {
    # "tutorial.pipelines.ProxyPipeline": 300,
    # "tutorial.piplines.MongoDBPipeline": 301,
}


"""以下时自定义配置"""

# 使用之前在http://www.xicidaili.com/网站爬取到的代理
HTTPPROXY_PROXY_LIST_FILE = 'proxy.json'

# 行情中心的配置
CENTER_LIST_FILE = 'center.json'


# MongoDB配置
MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DBNAME = "dfcf"  # db数据库名：东方财富
MONGODB_DOCNAME = "hqzx"  # collection文档名：行情中心

# Redis配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

# MySQL配置
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "rootroot"
MYSQL_DBNAME = "dfcf"

# Kafka配置
KAFKA_HOSTS = [
    "192.168.222.136:9092",
]

# Zookeeper配置
ZOOKEEPER_HOSTS = [
    "192.168.222.136",
]