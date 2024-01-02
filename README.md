Tech task +- 8h  

## Step 1: Data ingestion
Scrape jobs from using scrapy
Usajobs.gov: https://developer.usajobs.gov/Tutorials/Search-Jobs 

## Step2: Expose data via API
Expose example job search endpoints exposed via swagger.

## Technology used:  
- Python 3.12  
  - poetry for package management   
  - scrapy for performing requests efficiently   
  - scrapy pipelines to allow injecting middlewares, pipelines easily. In the future would be easy to save cache of visited websited in middleware that runs for every request. 
  - fastAPI + pydantic for api 
- elasticsearch as database because of searching needs like:
  - keyword search
  - performing aggregate functions like showing latest,newest for specific filter
  - allowing to index fields with custom analyzer like for keywords and making sure "ENGINEER", "engineer" both return the same results  
- Postgres/MySQL would not handle keywords searches as efficiently and there'd be need to do some custom work like preparing table with keywords mapping it with specific records etc and still not get as performant db as ES  
- docker/Docker-compose
  - completely minimalistic approach due to time constraints  


## Keyword strategy:
- One of key parts of this project is making sure searches are efficient.   
  - use standard analyzer for `job_title` - that allows searching for jobs that contain specific `keywords` with `AND`. It means for `[Software,Engineer]` keywords job titles like `Senior Software Engineer` are found but not `Aerospace Engineer`  
  - for location_name in jobs I am using custom analyzer that lowercases the string and removes dots so it allows at least to find `San Diego California` when in job description there was `San Diego, California` - handling location is not obvious in this case. It can be handled differently maybe with geolocation but due to time constraints I decided to leave my current basic solution  


 

## How to run:
- Rename `.env_template` to `.env` and update values. I am not storing my key on repo due to security concerns.  
  - `USAJOBS_API_KEY="xxxx="` - **this is the only necessary change- make sure you use active USAJOBS_API_KEY**
  - `ELASTICSEARCH_URL="http://elasticsearch:9200"` - no need to touch for test - it's pointing to service in docker-compose  
  - `PULL_LATEST_ONLY=false` - this allows to pull only last 10k - by default script pulls all records by selecting different salary ranges  
- Make sure port 9200 and 8000 are not being currently used by your processes.  
- Run command `make run-all-docker` - it should pull necessary elasticsearch image and build both api and etl container  
- Docker-compose makes sure elasticsearch responds with valid healthcheck before starting both `api` and `etl`. 
- Access http://localhost:8000/docs for swagger api that allows testing.
- ETL starts the same time as API - you can already query but results will change - to make sure all records are in DB you can see `etl` container logs. It'll kill container after completing.   


## Comments:
- To run latest jobs only make sure to run `etl` container with `PULL_LATEST_ONLY=True` env variable.  
- Elasticsearch does not keep the data after killing - on prod I'd use different ES setup with security on and ideally managed service.  Can be solved by mounting volume but to avoid any possible issues with your filesystem I decided to skip it for this task.   
- Simple tests are added but require setup to run - make sure you have python 3.12 locally with poetry. I have only 3 tests in place all of them are passing right now.  
- More tests require a bit more time but the plan would be to create elasticsearch container with testcontainers and make sure all cases are tested before going to production - especially foreign letters, all of basic cases  
- About metrics asked in task - I somehow skipped that important step and I don't have enough time to finish it. The idea was to have `scrape-session` and all of the records that are collected in one sessions are grouped.
- We can run query to get those metrics from ES but i didn't implement them inside code yet.
