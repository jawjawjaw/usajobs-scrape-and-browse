from fastapi import APIRouter, Depends
from services.job_service import JobService
from fastapi import Depends
from routers.dependencies import get_es_job_service
from services.job_service import JobService
from . import schema

router = APIRouter()


@router.post(
    "/jobs",
    response_model=schema.JobsSummaryResponse,
)
def get_jobs(
    job_query: schema.JobSearchQuery,
    job_service: JobService = Depends(get_es_job_service),
):
    resp = job_service.get_jobs(job_query.location, job_query.keywords)

    response_data = schema.JobsSummaryResponse(
        number_of_jobs=resp.number_of_jobs,
        oldest_job=schema.JobDetails(
            title=resp.oldest_job.title,
            posted_date=resp.oldest_job.posted_date,
        )
        if resp.oldest_job
        else None,
        newest_job=schema.JobDetails(
            title=resp.newest_job.title,
            posted_date=resp.newest_job.posted_date,
        )
        if resp.newest_job
        else None,
    )
    return response_data
