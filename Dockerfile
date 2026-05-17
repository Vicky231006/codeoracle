FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY ingest/requirements.txt /app/ingest/requirements.txt
COPY agents/requirements.txt /app/agents/requirements.txt
COPY api/requirements.txt /app/api/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ingest/requirements.txt && \
    pip install --no-cache-dir -r agents/requirements.txt && \
    pip install --no-cache-dir -r api/requirements.txt

# Copy application code
COPY . /app/

# Create directories for data and logs
RUN mkdir -p /app/data /app/logs

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run API server
CMD ["python", "run_api.py"]

# Made with Bob
