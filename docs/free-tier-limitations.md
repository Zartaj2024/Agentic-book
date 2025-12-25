# Free Tier Limitations and Considerations

This document outlines the limitations and considerations when running the Physical AI Book system on free-tier services.

## Service Limitations

### Qdrant Cloud (Free Tier)
- **Vector Storage**: Up to 100K vectors
- **API Calls**: Up to 100K calls per month
- **Data Storage**: Limited storage capacity
- **Performance**: Shared resources with potential throttling during peak usage

### Neon Postgres (Serverless)
- **Data Storage**: Up to 1GB
- **Compute Time**: Limited free compute time per month
- **Row Limit**: Up to 10M rows in any table
- **Connection Limits**: May have concurrent connection restrictions

### LLM APIs (Free Tier)
- **Groq/Gemini**: Limited requests per minute and per day
- **Rate Limits**: Requests may be throttled during high usage
- **Token Limits**: Restrictions on input/output token counts
- **Usage Quotas**: Daily/monthly usage caps

### GitHub Pages
- **Bandwidth**: Unlimited for public repositories
- **Storage**: 1GB per site
- **Build Minutes**: Limited Actions minutes per month (1000 free)
- **Custom Domains**: Supported but may have limitations

## System-Level Limitations

### Rate Limiting
The system implements rate limiting to stay within free tier constraints:
- Chat endpoint: 10 requests per minute per IP
- Ingestion endpoint: 5 requests per hour per IP
- General endpoints: 100 requests per minute per IP

### Monitoring
The system tracks usage through the monitoring endpoint (`/api/v1/monitoring/usage`) to ensure limits are not exceeded.

### Performance Considerations
- Cold starts for serverless functions may cause delays
- Vector database queries may be slower during peak usage
- LLM responses may be delayed during high usage periods

## Mitigation Strategies

### Caching
- Implement response caching for frequently asked questions
- Cache vector search results where appropriate
- Use browser caching for static assets

### Resource Optimization
- Optimize embeddings to reduce vector database usage
- Implement efficient chunking to minimize redundant storage
- Use compression for data transmission

### Graceful Degradation
- Implement fallback responses when LLM APIs are unavailable
- Provide offline access to core content
- Queue requests during high-usage periods

## Recommendations for Scale

If usage exceeds free tier limits, consider:

### Upgraded Services
- Upgrade to paid Qdrant tier for higher limits
- Use paid Neon Postgres tier for more storage/compute
- Upgrade LLM API tier for higher rate limits

### Optimization
- Implement more aggressive caching
- Optimize queries and reduce redundant operations
- Use CDN for static content delivery

### Architecture Changes
- Add load balancing for higher availability
- Implement database read replicas
- Use message queues for non-critical operations

## Monitoring and Alerts

Monitor these key metrics:
- API request volume vs. free tier limits
- Vector database usage and query performance
- LLM API usage and response times
- Database storage and connection usage

The system includes a monitoring endpoint at `/api/v1/monitoring/usage` that provides real-time usage statistics.