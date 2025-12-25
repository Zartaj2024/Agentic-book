@echo off
REM Docker setup batch file for Physical AI Book

echo ===========================================
echo Physical AI Book - Docker Setup Assistant
echo ===========================================

echo.
echo This script will help you set up the Docker environment for the Physical AI Book project.
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first:
    echo    https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('docker --version') do set docker_version=%%i
    echo ✅ Docker is installed: %docker_version%
)

REM Check if Docker Compose is available
docker compose version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not available. Please ensure Docker Compose V2 is enabled in Docker Desktop settings.
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('docker compose version') do set compose_version=%%i
    echo ✅ Docker Compose is available: %compose_version%
)

echo.
echo Setting up the project...

REM Copy .env.example to .env if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from example...
    copy .env.example .env >nul
    echo    Please edit .env with your specific configuration before running the services.
) else (
    echo ✅ .env file already exists.
)

echo.
echo 🚀 To start the services, run:
echo    docker-compose up --build
echo.
echo 📖 For detailed instructions, see DOCKER_INTEGRATION.md
echo.
echo 📋 Available commands:
echo    docker-compose up --build     ^# Build and start all services
echo    docker-compose up -d          ^# Start in detached mode
echo    docker-compose logs -f        ^# View logs in real-time
echo    docker-compose down           ^# Stop all services
echo    docker-compose down -v        ^# Stop and remove volumes
echo.
echo 🌐 Services will be available at:
echo    - Frontend (Docusaurus): http://localhost:3000
echo    - Backend (FastAPI): http://localhost:8000
echo    - Backend Health: http://localhost:8000/health
echo    - Qdrant Dashboard: http://localhost:6333
echo.
pause