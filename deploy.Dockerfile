本地端測試
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

# FROM python:3.12-slim

# WORKDIR /app

# COPY requirements.txt .

# RUN apt-get update && apt-get install -y build-essential && \
#     pip3 install --upgrade pip && \
#     pip3 install -r requirements.txt && \
#     pip3 install gunicorn uvicorn

# COPY . .

# ENV PORT=${PORT:-8080}
# EXPOSE 8080

# CMD ["bash", "-c", "gunicorn line_bot.line_bot_main:app -k uvicorn.workers.UvicornWorker -b :${PORT} --access-logfile - --error-logfile -"]
# # CMD ["gunicorn", "line_bot.line_bot_main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", ":8080"]
