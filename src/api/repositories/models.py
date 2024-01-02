from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# Pydantic model for job details
class JobDetails(BaseModel):
    title: str  # Job title
    posted_date: datetime  # Posted date of the job


class JobsSummaryResponse(BaseModel):
    number_of_jobs: int  # Number of jobs found
    oldest_job: Optional[JobDetails] = None  # Details of the oldest job
    newest_job: Optional[JobDetails] = None  # Details of the newest job


class OrganizationSummaryResponse(BaseModel):
    number_of_jobs: int  # Number of jobs found
    number_of_organizations: int  # Number of organizations found
    organizations: List[str]  # List of organizations found
