# ---- Builder stage: install dependencies ----
FROM python:3.11-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


# ---- Runtime stage ----
FROM python:3.11-slim

# Create a non-root user to run the app
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# Bring in packages installed in the builder stage
COPY --from=builder --chown=app:app /root/.local /home/app/.local

# Copy only what the runtime needs
COPY --chown=app:app app/ ./app/
COPY --chown=app:app frontend/ ./frontend/

ENV PATH=/home/app/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]