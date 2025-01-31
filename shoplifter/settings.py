# Scrapy settings for shoplifter project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "shoplifter"

SPIDER_MODULES = ["shoplifter.spiders"]
NEWSPIDER_MODULE = "shoplifter.spiders"

FEED = {
    'shoplofter.json': {
        "format": 'json',
        'overwrite': True
    }
}


SCRAPEOPS_API_KEY = ''

SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = "http://headers.scrapeops.io/v1/browser-headers"
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True

SCRAPEOPS_NUM_RESULTS = 50


# Enable the Redis scheduler
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# Ensure that the scheduler does not clean up the queue after crawling
SCHEDULER_PERSIST = True
# Use Redis for the duplicate filter to prevent re-scraping the same items
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# Redis connection parameters
REDIS_URL = 'redis://localhost:6379' 
REDIS_ENCODING = 'utf-8'

# Optional: Set up the Redis key for the start URLs
REDIS_START_URLS_KEY = 'shoplifter:start_urls'


MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'shoplifter_db'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'rootpassword'
MYSQL_PORT = 3306

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "shoplifter (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
#    "shoplifter.middlewares.ShoplifterSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "shoplifter.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware": 400,
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapy_splash.SplashMiddleware': 725,
    # 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Optional: Define a list of proxies
# PROXIES = [
#     "http://proxy1.example.com",
#     "http://proxy2.example.com",
# ]

# proxy list
ROTATING_PROXY_LIST_PATH = './http.txt'

# # Using Splash
# SPLASH_URL = 'http://http://127.0.0.1:8050/'

# # Settings for Splash
# DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'
# HTTPCACHE_STORAGE = 'scrapy_splash.DummyHTTPCacheStorage'
# REQUEST_FINGERPRINTER_CLASS = 'scrapy_splash.SplashRequestFingerprinter'


# # Timeouts and splash settings
# SPLASH_COOKIES_ENABLED = False
# SPLASH_DELAY = 2


# Error Handling and Retries: Handle HTTP errors like 404, 500, etc., by enabling retries
RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 429]
RANDOMIZE_DOWNLOAD_DELAY = True



# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
#    "shoplifter.pipelines.ShoplifterPipeline": 300,
#    "shoplifter.pipelines.MySQLPipeline": 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# # LOGGING
LOG_LEVEL = 'DEBUG'
LOG_FILE = './scrapy_log.log'