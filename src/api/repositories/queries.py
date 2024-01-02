from typing import Dict, List, Optional


def get_jobs_summary_query(location: str, keywords: Optional[List[str]] = None) -> Dict:
    """Returns es query for getting summary of jobs in a location."""
    job_title_query = " ".join(keywords) if keywords else None

    jobs_summary_query = {
        "size": 0,
        "query": {
            "bool": {
                "must": [],
                "filter": [
                    {
                        "nested": {
                            "path": "location",
                            "query": {"match_phrase": {"location.name": f"{location}"}},
                        }
                    }
                ],
            }
        },
        "aggs": {
            "oldest_job": {
                "terms": {"field": "posted_at", "size": 1, "order": {"_key": "asc"}},
                "aggs": {
                    "oldest_title": {
                        "top_hits": {"size": 1, "_source": {"includes": ["job_title"]}}
                    }
                },
            },
            "newest_job": {
                "terms": {"field": "posted_at", "size": 1, "order": {"_key": "desc"}},
                "aggs": {
                    "newest_title": {
                        "top_hits": {"size": 1, "_source": {"includes": ["job_title"]}}
                    }
                },
            },
        },
    }

    # Add keywords filter if keywords are present
    if job_title_query:
        jobs_summary_query["query"]["bool"]["filter"].append(
            {
                "match": {
                    "job_title": {
                        "query": f"{job_title_query}",
                        "operator": "and",
                    }
                }
            }
        )

    return jobs_summary_query


def get_organization_summary_query(location_name: str, location_state: str) -> Dict:
    """Returns es query for getting summary of organisation in a location."""
    return {
        "size": 10,
        "query": {
            "bool": {
                "must": [],
                "filter": [
                    {
                        "nested": {
                            "path": "location",
                            "query": {"match": {"location.name": f"{location_name}"}},
                        },
                    },
                    {
                        "nested": {
                            "path": "location",
                            "query": {"match": {"location.state": f"{location_state}"}},
                        },
                    },
                ],
            }
        },
        "aggs": {
            "unique_organizations": {"cardinality": {"field": "organization"}},
            "organizations": {"terms": {"field": "organization", "size": 1000}},
        },
    }
