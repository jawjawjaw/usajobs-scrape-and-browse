from datetime import datetime
from typing import Dict, List, Optional

from elasticsearch import Elasticsearch
from repositories import models
from repositories.job_repository import JobRepository
from repositories.queries import get_jobs_summary_query, get_organization_summary_query


class ElasticsearchJobRepository(JobRepository):
    """Implementation of JobRepository using Elasticsearch as the data store."""

    def __init__(self, client: Elasticsearch):
        self.client = client

    @staticmethod
    def parse_organizations_summary_response(
        response: Dict,
    ) -> Optional[models.OrganizationSummaryResponse]:
        number_of_jobs = response["hits"]["total"]["value"]

        unique_organizations_count = response["aggregations"]["unique_organizations"][
            "value"
        ]

        organizations = [
            bucket["key"]
            for bucket in response["aggregations"]["organizations"]["buckets"]
        ]

        return models.OrganizationSummaryResponse(
            number_of_jobs=int(number_of_jobs),
            number_of_organizations=int(unique_organizations_count),
            organizations=organizations,
        )

    @staticmethod
    def parse_jobs_summary_response(
        response: Dict,
    ) -> Optional[models.JobsSummaryResponse]:
        num_jobs = response["hits"]["total"]["value"]

        oldest_job = None
        newest_job = None

        if num_jobs > 0:
            oldest_bucket = response["aggregations"]["oldest_job"]["buckets"][0]
            oldest_date = datetime.fromtimestamp(int(oldest_bucket["key"]) / 1000.0)
            oldest_title = oldest_bucket["oldest_title"]["hits"]["hits"][0]["_source"][
                "job_title"
            ]

            newest_bucket = response["aggregations"]["newest_job"]["buckets"][0]
            newest_date = datetime.fromtimestamp(int(newest_bucket["key"]) / 1000.0)
            newest_title = newest_bucket["newest_title"]["hits"]["hits"][0]["_source"][
                "job_title"
            ]

            oldest_job = {"title": oldest_title, "posted_date": oldest_date}
            newest_job = {"title": newest_title, "posted_date": newest_date}

        return models.JobsSummaryResponse(
            number_of_jobs=num_jobs,
            oldest_job=oldest_job,
            newest_job=newest_job,
        )

    def get_organizations_summary(
        self, city: str, state: str
    ) -> models.OrganizationSummaryResponse:
        """Get summary of organizations in a city and state using elasticsearch client."""
        query = get_organization_summary_query(city, state)
        resp = self.client.search(index="jobs", body=query)
        return self.parse_organizations_summary_response(resp)

    def get_jobs_summary(
        self, location: str, keywords: Optional[List[str]] = None
    ) -> models.JobsSummaryResponse:
        """Get summary of jobs in a location using elasticsearch client."""
        query = get_jobs_summary_query(location, keywords)
        resp = self.client.search(index="jobs", body=query)
        return self.parse_jobs_summary_response(resp)
