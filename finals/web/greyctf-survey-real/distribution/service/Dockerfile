# Use a base image with Python 3.10 and Node.js
FROM python:3.10-slim-buster as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a new user 'ctf'
RUN useradd -m ctf

# Set working directory
WORKDIR /app

COPY . /app

RUN chmod 666 votes.json

# Switch to the 'ctf' user
USER ctf

# Install Flask and Gunicorn and requests
RUN pip install --upgrade pip \
    && pip install --no-cache-dir Flask gunicorn requests lxml

# Expose the Gunicorn port
EXPOSE 8000

# Command to run the Flask application using Gunicorn with 8 worker processes
CMD ["python3", "-m", "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "8", "main:app"]