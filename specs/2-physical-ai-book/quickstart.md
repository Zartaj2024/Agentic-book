# Quickstart Guide: Physical AI Book

**Feature**: Physical AI Book (2-physical-ai-book)
**Created**: 2025-12-10
**Status**: Draft

## Overview

This guide provides step-by-step instructions to set up and run the Physical AI Book project locally. The project consists of a Docusaurus frontend with AI chat capabilities and a FastAPI backend that implements RAG (Retrieval Augmented Generation) functionality.

## Prerequisites

- **Python 3.9+**: Required for the backend services
- **Node.js 18+**: Required for the Docusaurus frontend
- **Git**: For version control and cloning the repository
- **Access to LLM API**: Either Groq or Google Gemini API key
- **Qdrant Cloud Account**: For vector database storage
- **Neon Postgres Account**: For chat history storage

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd physical-ai-book
```

### 2. Backend Setup

#### Navigate to Backend Directory
```bash
cd backend
```

#### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```
If requirements.txt doesn't exist, install the required packages:
```bash
pip install fastapi uvicorn sentence-transformers qdrant-client python-dotenv psycopg2-binary
```

#### Configure Environment Variables
```bash
cp .env.example .env
```

Edit the `.env` file with your credentials:
```env
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_neon_postgres_connection_string
LLM_API_KEY=your_groq_or_gemini_api_key
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd ../docs-site  # From the backend directory
```

#### Install Dependencies
```bash
npm install
```

### 4. Content Preparation

#### Add Textbook Content
Place your textbook markdown files in the `/docs-site/docs/` directory:
- `01-intro-physical-ai.md`
- `02-humanoid-basics.md`
- `03-ros2-fundamentals.md`
- `04-digital-twins.md`
- `05-vla-systems.md`
- `06-capstone.md`

Ensure each file has proper headers (##, ###) for optimal RAG chunking.

## Running the Application

### 1. Start the Backend Service

From the `backend` directory:
```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`.

### 2. Populate the Vector Database

Before using the chat functionality, you need to ingest the textbook content:

```bash
cd scripts
python ingest.py
```

This will parse the markdown files, create embeddings, and upload them to Qdrant.

### 3. Start the Frontend Development Server

From the `docs-site` directory:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`.

## Testing the Application

### 1. Verify Backend API

Test the chat endpoint:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key" \
  -d '{"query": "What is forward kinematics?"}'
```

### 2. Test Frontend Features

- Navigate to `http://localhost:3000`
- Verify all textbook chapters are accessible
- Test the floating chatbot component
- Test the "Select-Text → Ask AI" feature by selecting text and clicking the tooltip

## Deployment

### Backend Deployment

Deploy to Render or Railway:
1. Create a new web service
2. Set the root directory to `/backend`
3. Add environment variables in the deployment settings
4. Set the start command to `uvicorn main:app:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment

Deploy to GitHub Pages:
1. Build the site: `npm run build`
2. Configure GitHub Pages in your repository settings
3. Set source to "GitHub Actions" or deploy the `build` folder manually

## Troubleshooting

### Common Issues

1. **API Rate Limits**: If you encounter rate limiting, check your LLM provider's usage dashboard
2. **Vector Database Connection**: Verify QDRANT_URL and QDRANT_API_KEY are correct
3. **Database Connection**: Ensure DATABASE_URL is properly formatted
4. **Content Not Appearing**: Check that markdown files are in the correct directory with proper headers

### Environment Variables Check

Verify all required environment variables are set:
```bash
# In the backend directory
python -c "import os; print('QDRANT_URL:', bool(os.getenv('QDRANT_URL')))"
python -c "import os; print('DATABASE_URL:', bool(os.getenv('DATABASE_URL')))"
python -c "import os; print('LLM_API_KEY:', bool(os.getenv('LLM_API_KEY')))"
```

## Next Steps

1. **Customize Content**: Add your specific textbook content to the `/docs` directory
2. **Fine-tune Prompts**: Adjust the system prompt in the backend for better educational responses
3. **Add Analytics**: Implement usage tracking to understand how students interact with the content
4. **Enhance UI**: Customize the Docusaurus theme and chatbot interface for your specific needs