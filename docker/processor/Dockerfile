FROM python:3.11-slim

WORKDIR /app

# Install poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Copy project files
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Copy source code
COPY src /app/src

# Add source directory to Python path
ENV PYTHONPATH=/app

CMD ["python", "-m", "src.processor.main"]