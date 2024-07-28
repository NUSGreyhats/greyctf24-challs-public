# Use a base image with Python 3.10 and Node.js
FROM python:3.10-slim-buster as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a new user 'ctf'
RUN useradd -m ctf

# Install curl
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Node Version Manager (NVM)
ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 18.0.0

RUN mkdir -p $NVM_DIR \
    && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

# Set Node.js path
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# Set working directory
WORKDIR /app

COPY . /app

# Switch to the 'ctf' user
USER ctf

# Install Flask and Gunicorn
RUN pip install --upgrade pip \
    && pip install --no-cache-dir Flask gunicorn

# Expose the Gunicorn port
EXPOSE 8000

# Command to run the Flask application using Gunicorn with 3 worker processes
CMD ["python3", "-m", "gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "proxy.main:app"]