FROM python:3.12-alpine AS prepare

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PACKAGES_CACHE_DIR=/tmp/packages_cache \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 

RUN pip install poetry==1.8.3

COPY pyproject.toml poetry.lock ./


FROM prepare AS dependencies

RUN if [ "$DOCKER_BUILDKIT" = "1" ]; then \
  echo "Building packages with buildkit cache"; \
  --mount=type=cache,target=$PACKAGES_CACHE_DIR poetry install --no-dev --no-root; \
  else \
  echo "Building packages default"; \
  poetry install --no-dev --no-root && rm -rf $POETRY_CACHE_DIR; \
  fi


FROM python:3.12-alpine AS squash

ENV VIRTUAL_ENV=/.venv
COPY --from=dependencies ${VIRTUAL_ENV} ${VIRTUAL_ENV}


FROM scratch

ENV PATH="/.venv/bin:$PATH" \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

WORKDIR /src
COPY ./src .
COPY --from=squash / /
