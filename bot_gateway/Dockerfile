# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY pyproject.toml .

# Install dependencies
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Copy the content of the local src directory to the working directory
COPY ./src .

# Command to run the application
CMD ["uvicorn", "bot_gateway.main:app", "--host", "0.0.0.0", "--port", "8000"]