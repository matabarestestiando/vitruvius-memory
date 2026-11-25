FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.7.5 /uv /usr/local/bin/uv
WORKDIR /srv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY memory ./memory
RUN useradd -u 10001 -M worker
USER worker
ENV PATH="/srv/.venv/bin:$PATH" PYTHONUNBUFFERED=1
CMD ["uvicorn","memory.main:app","--host","0.0.0.0","--port","8001","--no-access-log"]
