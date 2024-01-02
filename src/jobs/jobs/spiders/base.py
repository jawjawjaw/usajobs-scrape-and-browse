import scrapy


class BaseSpider(scrapy.Spider):
    raw_results_storage_cls = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_limit = kwargs.get("page_limit")
        self.raw_results_storage = kwargs.get("raw_results_storage")

    def save_raw_page(self, response, spider):
        self.raw_results_storage.save_raw_page(response, spider)
