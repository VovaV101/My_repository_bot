FROM python:3.10

WORKDIR /app

RUN pip install poetry

COPY bot_helper ./bot_helper
COPY pyproject.toml ./

RUN poetry install --no-dev --no-interaction --no-ansi


CMD ["poetry", "run", "bot_helper"]