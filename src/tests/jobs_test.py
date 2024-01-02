import pytest
from fastapi.testclient import TestClient

from main import app
from routers.dependencies import get_es_job_service
from routers.schema import JobsSummaryResponse, JobDetails, OrganizationSummaryResponse

client = TestClient(app)


@pytest.fixture
def mock_job_service():
    class MockJobService:
        def get_jobs(self, location, keywords):
            # Mock implementation of get_jobs method
            return JobsSummaryResponse(
                number_of_jobs=10,
                oldest_job=JobDetails(
                    title="Software Engineer",
                    posted_date="2022-01-03T00:00:00",
                ),
                newest_job=JobDetails(
                    title="Data Scientist/ Software Engineer",
                    posted_date="2023-01-03T00:00:00",
                ),
            )

        def get_organizations(self, city, state):
            # Mock implementation of get_jobs method
            return OrganizationSummaryResponse(
                number_of_jobs=10,
                number_of_organizations=2,
                organizations=["Org1", "Org2"],
            )

    return MockJobService()


def test_get_jobs(mock_job_service):
    # Mock the job_service dependency
    app.dependency_overrides[get_es_job_service] = lambda: mock_job_service

    # Send a POST request to the /jobs endpoint
    response = client.post(
        "api/jobs", json={ "keywords": ["software", "backend"]}
    )

    # Assert the response status code is 200
    assert response.status_code == 200

    # Assert the response JSON matches the expected data
    assert response.json() == {
        "number_of_jobs": 10,
        "oldest_job": {
            "title": "Software Engineer",
            "posted_date": "2022-01-03T00:00:00",
        },
        "newest_job": {
            "title": "Data Scientist/ Software Engineer",
            "posted_date": "2023-01-03T00:00:00",
        },
    }


def test_get_organizations(mock_job_service):
    # Mock the job_service dependency
    app.dependency_overrides[get_es_job_service] = lambda: mock_job_service

    # Send a POST request to the /jobs endpoint
    response = client.post(
        "api/organizations", json={"city": "San diego", "state": "California"}
    )

    # Assert the response status code is 200
    assert response.status_code == 200

    expected_response = {
        "number_of_jobs": 10,
        "number_of_organizations": 2,
        "organizations": ["Org1", "Org2"],
    }

    # Send request to the API

    # Check response status code
    assert response.status_code == 200

    # Check response data
    assert response.json() == expected_response
