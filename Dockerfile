FROM python:latest
WORKDIR /app
COPY pyproject.toml poetry.lock .env alembic.ini setup.cfg ./
COPY alembic alembic
COPY project_manager project_manager

RUN : \
    && python -m pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false

RUN poetry install --no-root --only main
CMD uvicorn project_manager.main:main_app --host 0.0.0.0 --port 8080
EXPOSE 8080
