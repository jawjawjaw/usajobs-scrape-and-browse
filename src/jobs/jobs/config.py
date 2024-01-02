import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment variable
USAJOBS_API_KEY = os.environ.get("USAJOBS_API_KEY", "")
PAGE_LIMIT = os.environ.get("PAGE_LIMIT", None)
ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL", "http://localhost:9200")
PULL_LATEST_ONLY = os.environ.get("PULL_LATEST_ONLY", False)