# PostgreSQL settings
POSTGRES_URI = 'localhost'  # Change this if needed
POSTGRES_DBNAME = 'odm_test'
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = '##########' # Use your own postgres password

# Enable the Postgres pipeline
ITEM_PIPELINES = {
    'imdb_scraper.pipelines.PostgresPipeline': 1,
}


# Scrapy settings for imdb_scraper project

BOT_NAME = "imdb_scraper"

SPIDER_MODULES = ["imdb_scraper.spiders"]
NEWSPIDER_MODULE = "imdb_scraper.spiders"

# General crawler settings
ROBOTSTXT_OBEY = False
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/108.0.0.0 Safari/537.36"
)
DEPTH_LIMIT = 0

# Downloader middlewares configuration
DOWNLOADER_MIDDLEWARES = {
    'imdb_scraper.middlewares.CustomProxyMiddleware': 700,  # Custom Proxy middleware
    'imdb_scraper.middlewares.CustomSeleniumMiddleware': 800,  # Custom Selenium middleware
}

# Selenium-specific settings
SELENIUM_PROXY_URL = "127.0.0.1:24000"
SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = r'/Users/masoud/Downloads/chromedriver'  # Update this path
SELENIUM_DRIVER_ARGUMENTS = [
    '--headless',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-extensions',
    '--no-sandbox',
    '--window-size=1920,1080',
    '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
]
SELENIUM_BROWSER_EXECUTABLE_PATH = None

# Request configuration
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


