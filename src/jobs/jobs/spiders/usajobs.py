import json
import os
import sys
from typing import Dict
import urllib
from uuid import uuid4

import scrapy
from jobs.spiders.base import BaseSpider

from jobs import items, utils

# Get the absolute path of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Append the relative path to the config module
sys.path.append(os.path.join(current_dir, ".."))

from config import USAJOBS_API_KEY, PULL_LATEST_ONLY


def get_filters():
    # Returns filters used for getting all of the results
    # in case it's not enough redefine filters in one placeß
    filters = []
    salary_low = 0
    salary_high = 10000
    for i in range(0, 20):
        filters.append(
            {
                "RemunerationMinimumAmount": salary_low,
                "RemunerationMaximumAmount": salary_high,
            }
        )
        salary_low += 10000
        salary_high += 10000
    # append one unlimited at the end to cover all jobs above 200k+
    max_expected_salary = 20000000
    filters.append(
        {
            "RemunerationMinimumAmount": salary_low,
            "RemunerationMaximumAmount": max_expected_salary,
        }
    )
    return filters


class USJobsSpider(BaseSpider):
    name = "usajobs"
    start_urls = ["https://data.usajobs.gov/api/Search"]
    page_size = 500
    base_url = start_urls[0]
    scrape_session = str(uuid4())

    @property
    def headers(self):
        return {
            "Authorization-Key": USAJOBS_API_KEY,
            "Content-Type": "application/json",
        }

    def start_requests(self):
        # Example filters and pagination
        if str(PULL_LATEST_ONLY).lower() == "true":
            self.logger.warning(
                "PULL_LATEST_ONLY is set to True - PULLING 10k LATEST JOBS ONLY"
            )
            filters = [{"SortField:": "opendate", "SortDirection": "asc"}]
        else:
            filters = get_filters()

        # Pagination settings
        for filter_data in filters:
            query_params = {
                "ResultsPerPage": str(self.page_size),
                "Page": "1",  # Start with the first page
                **filter_data,
            }

            # Append query string to the URL
            query_string = urllib.parse.urlencode(query_params)

            # Join base URL with query string
            url = urllib.parse.urljoin(self.base_url, f"?{query_string}")
            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse,
                meta={"filter_data": query_params, "page": 1},
            )

    def parse(self, response):
        data = json.loads(response.body)
        filter_data = response.meta["filter_data"]
        page = response.meta["page"]

        # Parse and extract job listings from the response JSON
        job_listings = data.get("SearchResult", {}).get("SearchResultItems", [])
        total_count = data.get("SearchResult", {}).get("SearchResultCountAll")

        if total_count == 10000:
            self.logger.warning(
                f"***Search results are limited to 10000. Please use filters to narrow down the search results.***"
            )
        self.logger.info(f"Total jobs found: {total_count} for filters {filter_data}")
        # Process job listings or yield items
        for job in job_listings:

            yield items.JobsItem(
                scrape_session=self.scrape_session,
                job_id=job.get("MatchedObjectId"),
                job_title=job.get("MatchedObjectDescriptor", {}).get("PositionTitle"),
                organization=job.get("MatchedObjectDescriptor", {}).get(
                    "OrganizationName"
                ),
                posted_at=utils.strip_date(
                    job.get("MatchedObjectDescriptor", {}).get("PublicationStartDate")
                ),
                location=[
                    items.LocationItem(
                        location_name=loc.get("LocationName"),
                        location_state=loc.get("CountrySubDivisionCode"),
                    )
                    for loc in job.get("MatchedObjectDescriptor", {}).get(
                        "PositionLocation", []
                    )
                ],
            )
        # Check if there are more pages
        total_pages = (
            data.get("SearchResult", {}).get("UserArea", {}).get("NumberOfPages", 0)
        )
        if int(total_pages) > int(page):
            page = int(page) + 1
            query_params = {
                **filter_data,
                "ResultsPerPage": str(self.page_size),
                "Page": str(page),  # Start with the first page
            }

            # Append query string to the URL
            query_string = urllib.parse.urlencode(query_params)

            # Join base URL with query string
            url = urllib.parse.urljoin(self.base_url, f"?{query_string}")

            yield scrapy.Request(
                url=url,
                headers=self.headers,
                callback=self.parse,
                meta={"filter_data": query_params, "page": page},
            )
