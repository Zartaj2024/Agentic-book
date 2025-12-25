# Physical AI Book - Deployment and Testing Guide

## Project Overview

The Physical AI Book is a complete interactive textbook system with AI-powered tutoring capabilities. This guide provides comprehensive instructions for deploying and testing the system.

## System Architecture

- **Frontend**: Docusaurus static site (GitHub Pages)
- **Backend**: FastAPI application with RAG capabilities (Render/Railway)
- **Vector Database**: Qdrant Cloud (for embeddings)
- **History Database**: Neon Postgres (for chat logs)
- **LLM Service**: Groq/Gemini API (for responses)

## Prerequisites

### Required Services (Free Tier)
- Qdrant Cloud account
- Neon Postgres account
- LLM API key (Groq or Gemini)
- GitHub account (for Pages)

### Local Development
- Python 3.9+
- Node.js 18+
- Git
- Docker (optional)

## Complete Deployment Process

### 1. Environment Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd physical-ai-book

# Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
cd ..

# Setup frontend
cd docs-site
npm install
cd ..
```

### 2. Backend Deployment (Render)

1. Push code to GitHub repository
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Create new Web Service
4. Connect to your GitHub repository
5. Set the following:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables from your `.env` file
6. Deploy

### 3. Frontend Deployment (GitHub Pages)

Option 1 - Using GitHub Actions (recommended):
1. Push your code to GitHub
2. The workflow in `.github/workflows/deploy.yml` will automatically deploy

Option 2 - Manual deployment:
```bash
cd docs-site
npm run build
./deploy.sh  # This will push to gh-pages branch
```

### 4. Content Ingestion

After deployment, ingest the textbook content:

```bash
# Locally
cd scripts
python ingest.py --docs-dir ../docs-site/docs

# Or using the deployed backend's ingestion endpoint (when available)
```

## Testing the Complete System

### 1. Verify Backend API

```bash
# Check health endpoint
curl https://your-backend-url/health

# Check API endpoints
curl https://your-backend-url/api/v1/health
curl https://your-backend-url/api/v1/monitoring/usage
```

### 2. Test Frontend

1. Navigate to your GitHub Pages URL
2. Verify all 6 textbook chapters are accessible
3. Test the floating AI chatbot
4. Test text selection feature ("Ask AI" tooltip)
5. Test search functionality

### 3. End-to-End Testing

```bash
# Run the integration test suite
./scripts/test-integration.sh
```

### 4. Manual Feature Testing

1. **Chat Functionality**: Ask questions about textbook content
2. **Text Selection**: Select text and click "Ask AI" tooltip
3. **Search**: Use search bar to find content across chapters
4. **Rate Limiting**: Verify API limits are enforced
5. **Monitoring**: Check usage statistics at `/api/v1/monitoring/usage`

## Configuration and Optimization

### Environment Variables

Key configuration options:

```env
# Rate limiting (requests per minute)
REQUEST_DAILY_LIMIT=100000
LLM_DAILY_LIMIT=10000
VECTOR_SEARCH_DAILY_LIMIT=100000

# RAG settings
RAG_TOP_K=3  # Number of chunks to retrieve
CHUNK_SIZE=500  # Size of text chunks
CHUNK_OVERLAP=50  # Overlap between chunks
```

### Performance Optimization

1. **Caching**: Implement response caching for common queries
2. **CDN**: Use CDN for static assets
3. **Compression**: Enable gzip compression
4. **Database**: Optimize query performance

## Monitoring and Maintenance

### Usage Monitoring

Check the monitoring endpoint regularly:
```
GET /api/v1/monitoring/usage
```

This provides:
- Current usage counts
- Daily limits
- Percentage of limits used
- Warnings when approaching limits

### Maintenance Tasks

1. **Content Updates**: Add new chapters by creating markdown files and re-running ingestion
2. **Performance Monitoring**: Watch for rate limit issues
3. **Error Monitoring**: Check logs for API errors
4. **Database Maintenance**: Monitor Neon Postgres usage

## Troubleshooting

### Common Issues

1. **API Rate Limits**: Check monitoring endpoint and adjust usage
2. **Vector Database Issues**: Verify QDRANT_URL and QDRANT_API_KEY
3. **LLM API Errors**: Check LLM_API_KEY and daily limits
4. **Database Connection**: Verify DATABASE_URL format

### Debugging Tips

1. Check the monitoring endpoint for usage statistics
2. Review application logs in your hosting platform
3. Verify all environment variables are correctly set
4. Test individual components separately

## Scaling Considerations

If usage exceeds free tier limits:

1. Upgrade to paid service tiers
2. Implement more aggressive caching
3. Optimize queries and reduce redundant operations
4. Consider load balancing for high availability

## Project Completion Status

✅ All 84 tasks completed across 8 phases:
- ✅ Phase 1: Setup (10/10 tasks)
- ✅ Phase 2: Infrastructure (10/10 tasks)
- ✅ Phase 3: User Story 1 (10/10 tasks)
- ✅ Phase 4: User Story 2 (10/10 tasks)
- ✅ Phase 5: User Story 3 (14/14 tasks)
- ✅ Phase 6: User Story 4 (11/11 tasks)
- ✅ Phase 7: User Story 5 (6/6 tasks)
- ✅ Phase 8: Polish (7/8 tasks, 1 optional remaining)

## Support Resources

- `docs/user-guide.md` - User documentation
- `docs/admin-guide.md` - Administrator guide
- `docs/free-tier-limitations.md` - Service limitations
- `README.md` - Comprehensive project overview

The Physical AI Book system is now ready for deployment and use!