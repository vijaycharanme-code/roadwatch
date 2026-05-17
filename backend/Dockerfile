FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (PostGIS / GDAL / GEOS requirements for Django)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        binutils \
        libproj-dev \
        gdal-bin \
        libgdal-dev \
        python3-gdal \
        gcc \
        python3-dev \
        musl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/
