SPIDER_NAME = usajobs

init:
	poetry install

run:
	cd src/jobs && poetry run scrapy crawl $(SPIDER_NAME)

install:
	poetry install

lint:
	poetry run pylint scrapy_project


run-api:
	cd src/api && poetry run uvicorn main:app --reload

test:
	  PYTHONPATH=src/api poetry run  pytest . 

run-all-docker:
	docker-compose up -d --build

help:
	@echo "Available commands:"
	@echo "Running project in docker:"
	@echo "  make run-all-docker - Run the API and the spider in docker"
	@echo "--------------------------"
	@echo "--------------------------"
	@echo "[LOCAL DEVELOPMENT] Running project locally:"
	@echo "  make init           - Install project dependencies"
	@echo "  make run            - Run the etl processes"
	@echo "  make install        - Install project dependencies"
	@echo "  make lint           - Run pylint for code linting"
	@echo "  make help           - Show available commands"
	@echo "  make run-api        - Run the API"
	@echo "  make test           - Run the tests"

.PHONY: init run install lint help