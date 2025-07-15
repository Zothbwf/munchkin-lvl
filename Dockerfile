FROM python:3.13.5

ARG YOUR_ENV

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=2.1.3

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry --version

WORKDIR /code/munchkin

COPY pyproject.toml poetry.lock /code/

RUN if [ "$YOUR_ENV" = "production" ]; then \
        poetry install --only=main --no-interaction --no-ansi; \
    else \
        poetry install --no-interaction --no-ansi; \
    fi

COPY . /code

EXPOSE 8000
CMD ["daphne", "munchkin.asgi:application", "-b", "0.0.0.0","-p","8000"]