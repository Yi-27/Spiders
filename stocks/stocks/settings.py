# Scrapy settings for stocks project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'stocks'

SPIDER_MODULES = ['stocks.spiders']
NEWSPIDER_MODULE = 'stocks.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'stocks (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'stocks.middlewares.StocksSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'stocks.middlewares.StocksDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'stocks.pipelines.StocksPipeline': 300,
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


# 换成scrapy_redis的调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 设置去重
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDipeFilter"

# 爬虫请求的调度算法 按情况三选一
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"  # 优先级算法

# 不清理Redis队列，好处是爬虫停止后再重新启动会从上次暂停的地方开始继续爬取
# 但是我们这里需要设置为False，即每读取一个URL后就删除一个，重新开始爬虫时会从头开始读取
SCHEDULER_PERSIST = False


DOWNLOAD_DELAY=2  # 固定延时2秒
# RANDOMIZE_DOWNLOAD_DELAY=True  # 随机的延迟时间

# 下载中间件
DOWNLOADER_MIDDLEWARES = {
    # 置于HttpProxyMiddleware(750)之前
    # 'tutorial.middlewares.RandomHttpProxyMiddleware':745,
    # 'tutorial.middlewares.ProxyMiddleware':745,  # 随机代理中间件
    "tutorial.middlewares.RandomUserAgentMiddleware": 380,  # 随机UA中间件
    # "tutorial.middlewares.HQZXHeadersMiddleware": 381,  # 设置请求头
    "tutorial.middlewares.DFCFSetCookiesMiddleware": 382,  # 设置cookies
}

# 爬虫中间件
SPIDER_MIDDLEWARES = {
   'tutorial.middlewares.HQZXStorageMiddleware': 543,
   # 'tutorial.middlewares.HQZXKafkaMiddleware': 543,
   # 'tutorial.middlewares.HQZXMongoMiddleware': 544,
}

# 激活管道
ITEM_PIPELINES = {
    # "tutorial.pipelines.ProxyPipeline": 300,
    # "tutorial.piplines.MongoDBPipeline": 301,
}





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
REDIS_HOST = "192.168.222.222"
REDIS_PORT = 6380
REDIS_PASSWORD = "redis_pwd"

# MySQL配置
MYSQL_HOST = "192.168.222.222"
MYSQL_PORT = 3307
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "root"
MYSQL_DBNAME = "dfcf"

# Kafka配置
KAFKA_HOSTS = [
    "192.168.222.222:9093",
]

# Zookeeper配置
ZOOKEEPER_HOSTS = [
    "192.168.222.222:2182",
]