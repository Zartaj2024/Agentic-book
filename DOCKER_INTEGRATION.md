# Docker Integration Guide

This project is configured for Docker-based development and deployment. Follow the instructions below to set up and run the application using Docker.

## Prerequisites

- Docker Engine (version 20.10 or higher)
- Docker Compose (v2 or higher)

Install Docker from [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Copy the example environment file:
```bash
cp .env.example .env
```

3. Edit the `.env` file with your configuration:
```bash
nano .env
```

4. Build and start the services:
```bash
docker-compose up --build
```

5. Access the applications:
   - Backend API: http://localhost:8000
   - Health check: http://localhost:8000/health
   - Docs Site: http://localhost:3000

## Available Services

- **Backend**: FastAPI application running on port 8000
- **Docs Site**: Docusaurus documentation site running on port 3000
- **Qdrant**: Vector database running on ports 6333 (HTTP) and 6334 (gRPC)

## Docker Compose Files

- `docker-compose.yml`: Development setup with volume mounts for live reloading
- `docker-compose.prod.yml`: Production setup optimized for deployment

## Development Commands

Build and run in development mode:
```bash
docker-compose up --build
```

Run in detached mode:
```bash
docker-compose up -d --build
```

View logs:
```bash
docker-compose logs -f
```

Stop services:
```bash
docker-compose down
```

Stop and remove volumes:
```bash
docker-compose down -v
```

Run only specific service:
```bash
docker-compose up --build backend
```

## Production Deployment

For production deployments, use the production compose file:

```bash
docker-compose -f docker-compose.prod.yml up --build
```

## Environment Variables

The application uses the following environment variables:

- `BACKEND_PORT`: Port for the backend service (default: 8000)
- `FRONTEND_PORT`: Port for the docs site (default: 3000)
- `QDRANT_URL`: URL for the Qdrant vector database
- `QDRANT_API_KEY`: API key for Qdrant (if authentication is enabled)
- `DATABASE_URL`: Connection string for the PostgreSQL database
- `LLM_API_KEY`: API key for the language model service
- `EMBEDDING_MODEL`: Model name for embeddings (default: all-MiniLM-L6-v2)

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the ports in `.env` file
2. **Permission errors**: Ensure Docker daemon is running with proper permissions
3. **Build failures**: Check that all required files exist in the project structure

### Service Health Checks

Check if all services are running:
```bash
docker-compose ps
```

Check logs for specific service:
```bash
docker-compose logs backend
docker-compose logs docs-site
docker-compose logs qdrant
```

### Resource Usage

Monitor resource usage:
```bash
docker stats
```

## Customization

### Backend Service
Located in `./backend/`, the FastAPI application can be customized by modifying:
- `main.py`: Main application entry point
- `routers/`: API route definitions
- `models/`: Data models
- `utils/`: Utility functions
- `requirements.txt`: Python dependencies

### Documentation Site
Located in `./docs-site/`, the Docusaurus site can be customized by modifying:
- `docs/`: Markdown documentation files
- `src/`: Custom React components
- `static/`: Static assets
- `docusaurus.config.js`: Site configuration
- `package.json`: Node.js dependencies

### Qdrant Vector Database
Qdrant is configured with persistent storage in the `qdrant_data` volume. The service exposes:
- HTTP API on port 6333
- gRPC API on port 6334
- Web UI accessible at http://localhost:6333/dashboard

## Building Images Manually

Build backend image:
```bash
cd backend
docker build -t agentic-book-backend .
```

Build docs site image:
```bash
cd docs-site
docker build -t agentic-book-docs .
```

## Cleanup

Remove all containers, networks, and volumes:
```bash
docker-compose down -v --remove-orphans
```

Remove unused Docker objects:
```bash
docker system prune
```

## Next Steps

Once your Docker setup is running:
1. Visit the API health endpoint at http://localhost:8000/health
2. Check the documentation site at http://localhost:3000
3. Verify Qdrant is accessible at http://localhost:6333/dashboard
4. Begin developing by modifying the source files (changes will be reflected in development mode)