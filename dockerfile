FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.3.0 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Install Poetry (PEP 621 compatible)
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

# Copy dependency manifests first (Docker layer caching)
COPY pyproject.toml poetry.lock* /app/

# Install runtime dependencies only (exclude dev group)
RUN poetry install --without dev --no-root --no-interaction --no-ansi

# Copy application source
COPY . /app/

# Ensure log directory exists (for rotating file handler)
RUN mkdir -p /app/logs

# Entrypoint
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
