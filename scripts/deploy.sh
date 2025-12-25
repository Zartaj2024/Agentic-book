#!/bin/bash

# Comprehensive deployment script for Physical AI Book
# Deploys both backend (to Render) and frontend (to GitHub Pages)

set -e  # Exit on any error

echo "==========================================="
echo "Physical AI Book Deployment Script"
echo "==========================================="

# Function to display usage
usage() {
    echo "Usage: $0 [backend|frontend|both|local]"
    echo "  backend  - Deploy only the backend to Render"
    echo "  frontend - Deploy only the frontend to GitHub Pages"
    echo "  both     - Deploy both backend and frontend (default)"
    echo "  local    - Deploy both services locally using Docker Compose"
    exit 1
}

# Check if we have the required tools
check_prerequisites() {
    if ! command -v git &> /dev/null; then
        echo "Error: git is required but not installed."
        exit 1
    fi

    case $1 in
        "backend")
            if ! command -v docker &> /dev/null; then
                echo "Error: docker is required for backend deployment."
                exit 1
            fi
            ;;
        "frontend")
            if ! command -v npm &> /dev/null; then
                echo "Error: npm is required for frontend deployment."
                exit 1
            fi
            ;;
        "local")
            if ! command -v docker &> /dev/null || ! command -v docker-compose &> /dev/null; then
                echo "Error: docker and docker-compose are required for local deployment."
                exit 1
            fi
            ;;
    esac
}

# Deploy backend to Render
deploy_backend() {
    echo "Deploying backend to Render..."

    # Check if Render CLI is installed
    if ! command -v render &> /dev/null; then
        echo "Render CLI not found. Please install it from: https://render.com/docs/cli"
        echo "Alternatively, you can deploy using Render's web dashboard."
        echo "Upload the backend directory and use the render.yaml configuration."
        return 1
    fi

    cd backend
    echo "Creating Render service..."
    render service create --name physical-ai-book-backend --type web --env python --region frankfurt
    echo "Backend deployment initiated via Render CLI."
    cd ..
}

# Deploy frontend to GitHub Pages
deploy_frontend() {
    echo "Deploying frontend to GitHub Pages..."

    cd docs-site

    # Check if we're in a git repository
    if [ ! -d .git ]; then
        echo "Error: Not in a git repository. Cannot deploy to GitHub Pages."
        cd ..
        return 1
    fi

    # Build the site
    echo "Building Docusaurus site..."
    npm run build

    # Deploy using git subtree
    git subtree push --prefix build origin gh-pages || {
        # If subtree push fails, try to create the branch first
        git subtree split --prefix build -b gh-pages
        git push -u origin gh-pages
    }

    echo "Frontend deployed to GitHub Pages!"
    cd ..
}

# Deploy both services locally using Docker Compose
deploy_local() {
    echo "Deploying both services locally using Docker Compose..."

    # Check if .env file exists, if not create from example
    if [ ! -f .env ]; then
        echo "Creating .env file from example..."
        cp backend/.env.example .env
        echo "Please update the .env file with your actual configuration before continuing."
        echo "After updating, run this script again."
        return 1
    fi

    # Build and start services
    echo "Starting services with Docker Compose..."
    docker-compose up --build -d

    echo "Services started successfully!"
    echo "Frontend should be available at: http://localhost:3000"
    echo "Backend should be available at: http://localhost:8000"
    echo "Qdrant dashboard should be available at: http://localhost:6333"
}

# Main execution
DEPLOY_TARGET=${1:-"both"}

check_prerequisites $DEPLOY_TARGET

case $DEPLOY_TARGET in
    "backend")
        deploy_backend
        ;;
    "frontend")
        deploy_frontend
        ;;
    "both")
        echo "Deploying both backend and frontend..."
        deploy_backend
        deploy_frontend
        ;;
    "local")
        deploy_local
        ;;
    *)
        usage
        ;;
esac

echo "==========================================="
echo "Deployment completed!"
echo "==========================================="