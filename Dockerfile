# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directory for the app user
RUN mkdir -p /home/app

# Create the app user
RUN groupadd -r app && useradd -r -g app app

# Create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Copy project
COPY . $APP_HOME

# Change ownership of all files to app user
RUN chown -R app:app $APP_HOME

# Change to the app user
USER app

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 