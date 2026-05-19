# Multi-stage build for Physical AI Book
# 1. Build the Docusaurus frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/docs-site
COPY docs-site/package*.json ./
RUN npm ci
COPY docs-site/ ./
RUN npm run build

# 2. Build the FastAPI backend and serve the frontend
FROM python:3.10-slim

# Create a non-root user for Hugging Face compatibility
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Install system dependencies (using root then switching back)
USER root
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY --chown=user backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY --chown=user backend/ ./backend/

# Copy built frontend from stage 1
COPY --chown=user --from=frontend-builder /app/docs-site/build ./frontend-build

# Switch back to the non-root user
USER user

# Set working directory to backend for execution
WORKDIR /app/backend

# Environment variables
ENV PORT=7860
ENV DOCUSAURUS_BACKEND_API_URL=""

# Expose port
EXPOSE 7860

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
