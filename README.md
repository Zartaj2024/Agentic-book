---
title: Physical AI Book
emoji: 📖
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# Physical AI Book

An interactive textbook that combines traditional educational content with AI-powered assistance for learning robotics and AI concepts.

## Overview

The Physical AI Book is an interactive textbook that provides students with both traditional reading material and AI-powered assistance. Students can read textbook content and ask questions to an AI tutor that responds based on the book's content using Retrieval Augmented Generation (RAG).

## Architecture

The system follows a monorepo structure:

```
/physical-ai-book
├── /docs-site       # Docusaurus Frontend (hosted on GitHub Pages)
├── /backend         # FastAPI + RAG Engine (hosted on Render/Railway)
├── /scripts         # Ingestion scripts
├── /docs            # Documentation files
├── .github/workflows # CI/CD workflows
└── README.md
```

### Tech Stack
- **Frontend**: Docusaurus (Static Site Generator) hosted on GitHub Pages
- **Backend**: FastAPI (Python) hosted on a free-tier PaaS (e.g., Render or Railway)
- **Vector Database**: Qdrant Cloud (Free Tier) for storing book embeddings
- **Database**: Neon (Serverless Postgres) for chat logs/analytics
- **LLM**: OpenAI, Groq, or Gemini API (Configurable) for flexible inference
- **Embeddings**: all-MiniLM-L6-v2 (Local/CPU-friendly)

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git
- Docker (optional, for containerized deployment)

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy the environment file: `cp .env.example .env`
6. Add your credentials to `.env` (see Environment Variables section below)

### Frontend Setup
1. Navigate to the docs-site directory: `cd docs-site`
2. Install dependencies: `npm install`
3. Start the development server: `npm start`

## Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```env
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_neon_postgres_connection_string
LLM_API_KEY=your_openai_groq_or_gemini_api_key
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-3.5-turbo
GROQ_MODEL=llama3-70b-8192
GEMINI_MODEL=gemini-pro
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=1000
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_DAILY_LIMIT=10000
VECTOR_SEARCH_DAILY_LIMIT=100000
REQUEST_DAILY_LIMIT=100000
DEBUG=false
```

## Deployment

### Backend Deployment (Render)

1. Push your code to a Git repository
2. Connect Render to your repository
3. Configure the following settings in Render:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables: Add all variables from your `.env` file
4. Use the `backend/render.yaml` file for automated configuration

### Frontend Deployment (GitHub Pages)

1. Build the site: `cd docs-site && npm run build`
2. Push to GitHub
3. Go to your repository settings > Pages
4. Set source to GitHub Actions or deploy the `build` folder manually
5. Alternatively, use the deployment script: `./docs-site/deploy.sh`

### Automated Deployment

Use the provided deployment scripts:

```bash
# Deploy both backend and frontend
./scripts/deploy.sh both

# Deploy only backend to Render
./scripts/deploy.sh backend

# Deploy only frontend to GitHub Pages
./scripts/deploy.sh frontend

# Run locally with Docker Compose
./scripts/deploy.sh local
```

### Local Development with Docker

1. Ensure Docker and Docker Compose are installed
2. Copy the example environment file: `cp .env.example .env`
3. Edit the `.env` file with your specific configuration
4. Run: `docker-compose up --build`

For production-like environment, use: `docker-compose -f docker-compose.prod.yml up --build`

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Health Check: http://localhost:8000/health
- Qdrant Dashboard: http://localhost:6333

Additional Docker commands:
- View logs: `docker-compose logs -f`
- Stop services: `docker-compose down`
- Stop and remove volumes: `docker-compose down -v`
- Run in detached mode: `docker-compose up -d --build`

## Content Management

### Adding New Chapters

1. Create a new markdown file in `docs-site/docs/`
2. Follow the naming convention: `NN-chapter-name.md` (e.g., `07-advanced-topics.md`)
3. Include proper headers (##, ###) to facilitate RAG chunking
4. Run the ingestion script to add content to the vector database

### Ingesting Content

To ingest textbook content into the vector database:

```bash
cd scripts
python ingest.py --docs-dir ../docs-site/docs
```

Force re-ingestion of all content:
```bash
python ingest.py --force
```

## Testing

### Integration Testing

Run the comprehensive integration test suite:

```bash
./scripts/test-integration.sh
```

This tests all major functionality including:
- Backend API endpoints
- Health checks
- Rate limiting
- File existence verification
- Component integration

### Manual Testing

1. Start both frontend and backend services
2. Navigate to the frontend URL
3. Verify all 6 textbook chapters are accessible
4. Test the AI chatbot functionality
5. Test the text selection feature
6. Verify search functionality works across all chapters

## Features

- Interactive textbook with 6 core chapters on robotics and AI
- AI-powered chatbot that responds based on textbook content
- Text selection feature to ask AI about specific content
- Search functionality across all textbook content
- Chat history logging for review
- Rate limiting to stay within free tier limits
- Usage monitoring and reporting
- Responsive design for mobile and desktop

## Free Tier Limitations

This system is designed to operate within free tier limits. See `docs/free-tier-limitations.md` for details on:
- Qdrant Cloud limitations
- Neon Postgres serverless limits
- LLM API rate limits
- GitHub Pages constraints
- Mitigation strategies

## Project Status

This project is complete with all planned features implemented:

1. ✅ Introduction to Physical AI
2. ✅ Humanoid Basics
3. ✅ ROS2 Fundamentals
4. ✅ Digital Twins
5. ✅ Vision-Language-Action Systems
6. ✅ Capstone Project

## Contributing

Contributions are welcome! Please read our contributing guidelines for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, see:
- `docs/user-guide.md` for user documentation
- `docs/admin-guide.md` for administrator documentation
- `docs/free-tier-limitations.md` for service limitations