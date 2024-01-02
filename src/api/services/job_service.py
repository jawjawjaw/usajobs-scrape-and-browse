from typing import List, Optional

from repositories import models
from repositories.job_repository import JobRepository


class JobService:
    def __init__(self, job_repo: JobRepository):
        self.job_repo = job_repo

    def get_organizations(
        self, city: str, state: str
    ) -> models.OrganizationSummaryResponse:
        return self.job_repo.get_organizations_summary(city, state)

    def get_jobs(
        self, location: str, keywords: Optional[List[str]] = None
    ) -> models.JobsSummaryResponse:
        return self.job_repo.get_jobs_summary(location, keywords)
