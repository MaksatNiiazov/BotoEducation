FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml /app/
COPY app /app/app

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir .

ENV PYTHONUNBUFFERED=1

CMD python -m uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT}
