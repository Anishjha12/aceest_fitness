# ──────────────────────────────────────────────────────────────
# ACEest Fitness & Gym – Docker Image
# ──────────────────────────────────────────────────────────────
FROM python:3.11-slim

LABEL maintainer="devops@aceest.com"
LABEL app="aceest-fitness"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Expose port
EXPOSE 5000

# Non-root user for security
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# Start application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "ACEest_Fitness:app"]
