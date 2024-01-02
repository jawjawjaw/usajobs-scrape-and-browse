# Base image
FROM python:3.12

# Set working directory
WORKDIR /app

# Copy only requirements to cache them in Docker layer
COPY pyproject.toml poetry.lock /app/

# Install poetry
RUN pip install poetry

# Install project dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY ./src/ /app
COPY ./scripts/ /app/scripts

CMD ["sh", "scripts/run-etl.sh"]