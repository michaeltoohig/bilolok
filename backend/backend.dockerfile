# FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# WORKDIR /app/

FROM python:3.8-slim AS python-poetry-base
# Default to the latest version of Poetry
ARG POETRY_VERSION=""

ENV POETRY_VERSION=${POETRY_VERSION}
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$PATH"

FROM python-poetry-base AS python-poetry-builder

RUN apt-get update \
    && apt-get install --no-install-recommends --assume-yes curl
# This script respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python3 -

FROM python-poetry-base AS python-poetry
COPY --from=python-poetry-builder $POETRY_HOME $POETRY_HOME

FROM python-poetry as app

WORKDIR /code

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./app/pyproject.toml ./app/poetry.lock* /code

RUN poetry install --no-root --only main

# Allow installing dev dependencies to run tests
# ARG INSTALL_DEV=false
# RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
# ARG INSTALL_JUPYTER=false
# RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

COPY ./app /code/app

ENV PYTHONPATH=/code

# CMD ["sleep", "3600"]

WORKDIR /code/app

# run entrypoint.sh
COPY ./entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

COPY ./start-reload.sh /code/start-reload.sh
RUN chmod +x /code/start-reload.sh

ENTRYPOINT [ "/code/entrypoint.sh" ]
# CMD ["../.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]