# AX Technology Test Project

## Development Setup

### Install virtual environment

- Create virtual environment with python 3.10
```python3.10 -m venv venv```
- Install requirements
```pip install -r requirements.txt```
- Configure environment variables
```cp .env.example .env``` and edit environment variables

### Configure local database

- Apply migrations
```alembic upgrade +1```
- Downgrading migrations
```alembic downgrade -1```
- Generating new migration files
```alembic revision -m "Write migration name" --autogenerate```

### Install pre-commit

- Install pre-commit ```pip install pre-commit```
- Install mypy ```pip install mypy```
- Apply pre-commit ```pre-commit install```
- Run pre-commit hooks ```pre-commit run --all-files```

### Run code in docker container

- Run docker-compose ```docker-compose up -d```

### Run tests

```pytest``` or ```pytest -vv```

### Documentation

```http://0.0.0.0:8000/redoc```