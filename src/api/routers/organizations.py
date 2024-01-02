from fastapi import APIRouter, Depends

from services.job_service import JobService
from routers.dependencies import get_es_job_service

from . import schema

router = APIRouter()


@router.post(
    "/organizations/",
    response_model=schema.OrganizationSummaryResponse,
)
def get_organizations(
    org_query: schema.OrganizationQuery,
    job_service: JobService = Depends(get_es_job_service),
):
    # Prepare response
    resp = job_service.get_organizations(org_query.city, org_query.state)
    response_data = schema.OrganizationSummaryResponse(
        number_of_jobs=resp.number_of_jobs,
        number_of_organizations=resp.number_of_organizations,
        organizations=resp.organizations,
    )
    return response_data
