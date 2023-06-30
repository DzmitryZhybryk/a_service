FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ARG INSTALL_COMMAND=i-prod
WORKDIR /code

COPY ./pyproject.toml ./pdm.lock /code/

RUN pip install pdm && \
    python -m pdm ${INSTALL_COMMAND}

COPY ./alembic.ini ./pytest.ini /code/
COPY ./app /code/app/
