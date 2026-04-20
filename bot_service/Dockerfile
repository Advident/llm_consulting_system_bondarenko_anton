FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir uv
RUN uv sync

CMD ["uv", "run", "python", "-m", "app.run_bot"]