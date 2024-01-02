from abc import ABC, abstractmethod
from typing import List, Optional

from repositories import models


class JobRepository(ABC):
    """Abstract class for JobRepository implementations."""

    @abstractmethod
    def get_organizations_summary(
        self, city: str, state: str
    ) -> models.OrganizationSummaryResponse:
        pass

    @abstractmethod
    def get_jobs_summary(
        self, location: str, keywords: Optional[List[str]] = None
    ) -> models.JobsSummaryResponse:
        pass
