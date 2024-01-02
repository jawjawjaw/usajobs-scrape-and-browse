from fastapi import FastAPI
from routers.jobs import router as job_router
from routers.organizations import router as organistaions_router

app = FastAPI()

app.include_router(job_router, prefix="/api")
app.include_router(organistaions_router, prefix="/api")
