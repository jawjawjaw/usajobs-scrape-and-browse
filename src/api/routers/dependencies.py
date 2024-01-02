from elasticsearch import Elasticsearch
from fastapi import Depends
from repositories.es_repository import ElasticsearchJobRepository
from services.job_service import JobService
from config import ELASTICSEARCH_URL
# from routers.organizations import router as organistaions_router


def get_es_jobs_repository():
    es = Elasticsearch(hosts=[ELASTICSEARCH_URL])
    job_repo = ElasticsearchJobRepository(client=es)
    return job_repo


def get_es_job_service(job_repo=Depends(get_es_jobs_repository)) -> JobService:
    return JobService(job_repo)
