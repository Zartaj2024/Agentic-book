# Administrator Guide for Physical AI Book

## Overview

This guide provides instructions for administrators managing the Physical AI Book system, including setup, configuration, monitoring, and maintenance tasks.

## System Architecture

The Physical AI Book system consists of:
- **Frontend**: Docusaurus-based static site hosted on GitHub Pages
- **Backend**: FastAPI application with RAG capabilities
- **Vector Database**: Qdrant Cloud for textbook embeddings
- **History Database**: Neon Postgres for chat logs
- **LLM Service**: Groq or Gemini API for inference

## Initial Setup

### Prerequisites

Before setting up the system, ensure you have:

- Qdrant Cloud account (free tier available)
- Neon Postgres account (free tier available)
- LLM API key (Groq or Gemini)
- GitHub account for hosting

### Environment Configuration

Create a `.env` file in the `backend` directory with the following variables:

```bash
QDRANT_URL=your_qdrant_cluster_url
QDRANT_API_KEY=your_qdrant_api_key
DATABASE_URL=your_neon_postgres_connection_string
LLM_API_KEY=your_groq_or_gemini_api_key
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_DAILY_LIMIT=10000
VECTOR_SEARCH_DAILY_LIMIT=100000
REQUEST_DAILY_LIMIT=100000
DEBUG=false
```

### Database Setup

The system will automatically create the required tables in your Neon Postgres database. The chat history table will be created on first use with the following schema:

```sql
CREATE TABLE chat_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_query TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    session_id UUID NOT NULL,
    context_used JSONB,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

## Content Management

### Adding New Chapters

To add new textbook chapters:

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

You can also force re-ingestion of all content:

```bash
python ingest.py --force
```

## Monitoring and Usage Tracking

### Checking API Usage

Monitor your API usage through the monitoring endpoint:

```
GET /api/v1/monitoring/usage
```

This endpoint returns:
- Current usage counts for requests, LLM calls, and vector searches
- Daily limits configured in environment variables
- Percentage of limits used
- Warning flags when approaching limits (>80%)

### Rate Limits

The system implements the following rate limits:
- Chat endpoint: 10 requests per minute per IP
- Ingestion endpoint: 5 requests per hour per IP
- General endpoints: 100 requests per minute per IP

## Deployment

### Backend Deployment

Deploy the backend to a PaaS platform (Render, Railway, etc.):

1. Push code to a Git repository
2. Connect your PaaS platform to the repository
3. Configure environment variables in the platform
4. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment

Deploy the frontend to GitHub Pages:

1. Build the site: `cd docs-site && npm run build`
2. Configure GitHub Pages in your repository settings
3. Set source to GitHub Actions or deploy the `build` folder manually

## Troubleshooting

### Common Issues

#### Rate Limit Exceeded
- Check the monitoring endpoint for usage statistics
- Adjust limits in environment variables if needed
- Implement additional caching if usage is consistently high

#### Vector Database Connection Issues
- Verify QDRANT_URL and QDRANT_API_KEY are correct
- Check that your Qdrant Cloud account is active
- Ensure the required collection exists (system creates it automatically)

#### LLM API Errors
- Verify LLM_API_KEY is correct
- Check that you haven't exceeded daily limits
- Ensure the correct API endpoint is being used

#### Database Connection Issues
- Verify DATABASE_URL is properly formatted
- Check that your Neon Postgres account is active
- Ensure required tables exist (they're created automatically)

### Logging

The system logs important events including:
- Database connection status
- Vector database operations
- API rate limit events
- Error conditions

Check application logs for troubleshooting information.

## Security Considerations

- Store API keys securely, never commit them to version control
- Use HTTPS for all API communications
- Implement proper authentication for administrative endpoints
- Monitor for unusual usage patterns

## Performance Optimization

- Use CDN for static frontend assets
- Implement caching for frequently accessed content
- Optimize database queries for chat history
- Monitor and adjust rate limits based on usage patterns

## Backup and Recovery

- Regularly backup your Neon Postgres database
- Maintain copies of your content markdown files
- Document your environment configurations
- Test recovery procedures periodically

This guide provides the essential information for managing the Physical AI Book system. For additional support, refer to the specific documentation for each component (FastAPI, Qdrant, Neon, etc.).