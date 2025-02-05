FROM python:latest
WORKDIR /app
COPY pyproject.toml poetry.lock .env alembic.ini setup.cfg ./
COPY alembic alembic
COPY project_manager project_manager

RUN : \
    && python -m pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false

ENV DB_HOST db
RUN poetry install --no-root --only main
CMD alembic upgrade head && uvicorn project_manager.main:main_app --host 0.0.0.0 --port 8080
EXPOSE 8080
