# Django Project

This is a Django project created with Django 4.2.20.

## Setup Instructions

Just run `docker compose up` to start the project. This will build the Docker image and start the Django development server.
Make sure you have Docker and Docker Compose installed on your machine.
You can also run the following command to build the Docker image without starting the server:

```bash
docker compose build
```
You can then run the server with:

```bash
docker compose up
```
This will start the server in the foreground. You can stop it with `Ctrl+C`.
If you want to run the server in detached mode (in the background), you can use:

```bash
docker compose up -d
```

The server will start at http://127.0.0.1:8000/

## Project Structure

- `myproject/` - Main project directory
  - `manage.py` - Django's command-line utility for administrative tasks
  - `myproject/` - Project configuration directory
    - `settings.py` - Project settings
    - `urls.py` - URL configuration
    - `wsgi.py` - WSGI configuration
    - `asgi.py` - ASGI configuration 