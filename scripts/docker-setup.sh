#!/bin/bash
# Docker setup script for Physical AI Book

echo "==========================================="
echo "Physical AI Book - Docker Setup Assistant"
echo "==========================================="

echo
echo "This script will help you set up the Docker environment for the Physical AI Book project."
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   - Docker Desktop: https://www.docker.com/products/docker-desktop"
    echo "   - Docker Engine: https://docs.docker.com/engine/install/"
    exit 1
else
    echo "✅ Docker is installed: $(docker --version)"
fi

# Check if Docker Compose is available
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please ensure Docker Compose V2 is enabled in Docker Desktop settings."
    exit 1
else
    echo "✅ Docker Compose is available: $(docker compose version)"
fi

echo
echo "Setting up the project..."

# Copy .env.example to .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "   Please edit .env with your specific configuration before running the services."
else
    echo "✅ .env file already exists."
fi

echo
echo "🚀 To start the services, run:"
echo "   docker-compose up --build"
echo
echo "📖 For detailed instructions, see DOCKER_INTEGRATION.md"
echo
echo "📋 Available commands:"
echo "   docker-compose up --build     # Build and start all services"
echo "   docker-compose up -d          # Start in detached mode"
echo "   docker-compose logs -f        # View logs in real-time"
echo "   docker-compose down           # Stop all services"
echo "   docker-compose down -v        # Stop and remove volumes"
echo
echo "🌐 Services will be available at:"
echo "   - Frontend (Docusaurus): http://localhost:3000"
echo "   - Backend (FastAPI): http://localhost:8000"
echo "   - Backend Health: http://localhost:8000/health"
echo "   - Qdrant Dashboard: http://localhost:6333"
echo