FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "exec gunicorn line_bot.line_bot_main:app -k uvicorn.workers.UvicornWorker -b :${PORT:-8080}"]
