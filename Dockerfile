FROM python:3.10

WORKDIR /app

RUN pip install poetry

COPY bot_helper/my_bot/ ./
RUN poetry install --no-dev --no-interaction --no-ansi

CMD ["python", "bot_helper/bot.py"]