FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /code

COPY ./pyproject.toml ./pdm.lock ./alembic.ini /code/
COPY ./app /code/app/

RUN pip install pdm && \
    python -m pdm install
