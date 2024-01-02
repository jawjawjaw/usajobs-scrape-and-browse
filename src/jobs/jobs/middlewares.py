# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# useful for handling different item types with a single interface
from elasticsearch import Elasticsearch
from itemadapter import ItemAdapter, is_item
from scrapy import signals
from config import ELASTICSEARCH_URL

class JobsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)

        return s

    def spider_opened(self, spider):
        spider.logger.info(
            f"Spider opened: {spider.name} - session: {spider.scrape_session}"
        )

    def spider_closed(self, spider):
       
        spider.logger.info("Spider closed: %s" % spider.name)
        spider.logger.info("Total jobs scraped: %s" % spider.scrape_session)
        spider.logger.info("Total locations scraped: %s" % spider.scrape_session)


class SaveRawPagesMiddleware:
    def process_response(self, request, response, spider):
        if "page" in request.meta:
            spider.save_raw_page(response, spider)
        return response

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
