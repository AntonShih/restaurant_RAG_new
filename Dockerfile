# Dockerfile
FROM python:3.12-slim

# 環境設定
WORKDIR /app
ENV POETRY_VERSION=1.8.2

# 安裝 Poetry
RUN pip install --no-cache-dir poetry==$POETRY_VERSION

# 複製 pyproject.toml 和 poetry.lock（讓 Docker 利用快取）
COPY pyproject.toml poetry.lock* /app/

# 安裝依賴（只安裝非 dev）
RUN poetry config virtualenvs.create false \
  && poetry install --no-root --only main

RUN poetry show uvicorn

# 複製剩下的原始碼
COPY . /app

# 啟動指令（確保 uvicorn 來自 Python module）
CMD ["python", "-m", "uvicorn", "line_bot.line_bot_main:app", "--host", "0.0.0.0", "--port", "8000"]
