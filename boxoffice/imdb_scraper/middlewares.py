from scrapy import signals
from scrapy_selenium.middlewares import SeleniumMiddleware
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

class ImdbScraperSpiderMiddleware:
    """Spider middleware for IMDB scraper."""
    
    @classmethod
    def from_crawler(cls, crawler):
        instance = cls()
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        return instance

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")

    def process_spider_output(self, response, result, spider):
        """Called with the results returned from the spider."""
        yield from result

class ImdbScraperDownloaderMiddleware:
    """Downloader middleware for IMDB scraper."""
    
    @classmethod
    def from_crawler(cls, crawler):
        instance = cls()
        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)
        return instance

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")

    def process_response(self, request, response, spider):
        """Called with the response returned from the downloader."""
        return response

class CustomProxyMiddleware:
    """Middleware to handle custom proxy setup."""
    
    def process_request(self, request, spider):
        request.meta['proxy'] = "127.0.0.1:24000"
        request.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9'
        })
        spider.logger.info("Using proxy: 127.0.0.1:24000")

class CustomSeleniumMiddleware(SeleniumMiddleware):
    """Custom Selenium middleware with proxy support."""
    
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        driver_options = webdriver.ChromeOptions()
        
        if proxy_url := settings.get("SELENIUM_PROXY_URL"):
            driver_options.add_argument(f"--proxy-server={proxy_url}")
            crawler.spider.logger.info(f"Proxy set: {proxy_url}")

        for argument in settings.get("SELENIUM_DRIVER_ARGUMENTS", []):
            driver_options.add_argument(argument)

        service = Service(settings.get("SELENIUM_DRIVER_EXECUTABLE_PATH"))
        driver = webdriver.Chrome(service=service, options=driver_options)
        return cls(driver)

    def __init__(self, driver):
        self.driver = driver
