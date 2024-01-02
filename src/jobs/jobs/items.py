# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LocationItem(scrapy.Item):
    # LocationItem is a single location of a job - e.g. San Francisco, California, United States
    location_name = scrapy.Field()
    # Location state stores state of the location e.g. California
    location_state = scrapy.Field()


class JobsItem(scrapy.Item):
    # TODO: add something like source is scraped source website because job_id is unique only on one website
    # scrape_session is unique per scrape session (each etl run)
    scrape_session = scrapy.Field()
    # job_title is scraped position title
    job_title = scrapy.Field()
    # organization is scraped organization name
    organization = scrapy.Field()
    # posted_at is scraped publication date
    posted_at = scrapy.Field()
    # location is scraped position location - a list of LocationItems
    location = scrapy.Field(serializer=LocationItem)
    # job_id is scraped job id - unique identifier on scraped website
    job_id = scrapy.Field()
