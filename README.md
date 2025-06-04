# testcodex

This repository contains a Django project. The steps below show how to run it in a local development environment.

## 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure environment variables

Copy the example file and adjust the values as needed. Set the database settings if you want to use Postgres instead of the default SQLite.

```bash
cp .env.example .env
# edit .env to suit your setup
```

## 4. Start Postgres and Redis

Docker Compose is provided to run Postgres and Redis containers during development.

```bash
docker-compose up -d
```

## 5. Apply database migrations

```bash
python manage.py migrate
```

## 6. (Optional) Create a superuser

```bash
python manage.py createsuperuser
```

## 7. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.
