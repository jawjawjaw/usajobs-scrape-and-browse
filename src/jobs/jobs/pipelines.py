import logging
from elasticsearch import Elasticsearch

from jobs import utils
from config import ELASTICSEARCH_URL
from scrapy.exceptions import DropItem
from elastic import mapping


class SaveJobsPipeline:
    # Take from config
    elasticsearch_url = ELASTICSEARCH_URL
    logger = logging.getLogger("elastic_transport.transport")
    logger.propagate = False

    def __init__(self):
        self.ids_seen = set()
        self.elasticsearch = Elasticsearch(self.elasticsearch_url)
        self.elasticsearch.indices.create(
            index="jobs", body=mapping, ignore=400
        )  # Create index with the specified mapping

    def process_item(self, item, spider):
        if item.get("job_id") in self.ids_seen:
            raise DropItem("Duplicate item id found: %s" % item.get("job_id"))
        else:
            self.ids_seen.add(item["job_id"])
            self.index_on_elasticsearch(item)
            return item

    def index_on_elasticsearch(self, item):
        item_data = {
            "scrape_session": item.get("scrape_session"),
            "job_id": item.get("job_id"),
            "job_title": item.get("job_title"),
            "organization": item.get("organization"),
            "posted_at": utils.strip_date(item.get("posted_at")),
            "location": [
                {
                    "name": i.get("location_name"),
                    "state": i.get("location_state"),
                }
                for i in item.get("location")
            ],
        }

        self.elasticsearch.index(index="jobs", id=item_data["job_id"], body=item_data)
