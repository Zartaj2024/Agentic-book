# Research Document: Physical AI Book Implementation

**Feature**: Physical AI Book (2-physical-ai-book)
**Created**: 2025-12-10
**Status**: Completed

## Research Summary

This document addresses the key unknowns and technical decisions needed for implementing the Physical AI Book project, including LLM provider selection, embedding model choice, and free-tier service limitations.

## Decision 1: LLM Provider Selection

### Decision: Use Groq API for LLM inference

### Rationale:
- **Cost**: Groq offers generous free tier for educational projects
- **Performance**: Groq provides faster inference times which is important for interactive learning
- **Quality**: Good performance on educational Q&A tasks
- **Integration**: Simple API integration with Python requests

### Alternatives Considered:
1. **Google Gemini API**: Good educational capabilities but potentially more restrictive free tier
2. **OpenAI API**: Higher quality but likely exceeds free tier limits quickly
3. **Open Source Models**: Could run locally but would require more infrastructure

### Final Recommendation: Groq API
- Best balance of cost, performance, and quality for educational use
- Sufficient free tier for student usage patterns
- Fast response times enhance learning experience

## Decision 2: Embedding Model Selection

### Decision: Use all-MiniLM-L6-v2 for embeddings

### Rationale:
- **Cost**: Can run locally without API costs, staying within budget
- **Performance**: Good semantic search quality for educational text
- **Efficiency**: Smaller model (384 dimensions) reduces vector database costs
- **Integration**: Easy to integrate with Python FastAPI backend using sentence-transformers

### Alternatives Considered:
1. **OpenAI text-embedding-3-small**: Higher quality but costs add up with usage
2. **Other Sentence Transformers**: Variants like all-mpnet-base-v2 offer higher quality but larger vectors

### Final Recommendation: all-MiniLM-L6-v2
- Optimal balance of quality and cost for free-tier operation
- 384-dimensional vectors keep Qdrant Cloud usage low
- Proven effectiveness for educational content similarity

## Decision 3: Free Tier Limitations Understanding

### Qdrant Cloud Free Tier:
- Up to 100K vectors
- Up to 100K API calls/month
- Sufficient for textbook content (estimated <10K chunks)

### Neon Postgres Serverless:
- Up to 10M rows in any table
- Up to 1GB data
- Sufficient for chat history with proper retention policies

### Groq API Free Tier:
- Generous limits for educational use
- Monitor usage and implement rate limiting if needed
- Estimated <1000 daily queries for educational use case

### GitHub Pages:
- Unlimited hosting for static content
- Perfect for Docusaurus frontend

## Decision 4: Architecture Considerations

### Frontend Performance:
- Docusaurus will pre-build static content for fast loading
- AI components will be loaded asynchronously to not block main content
- Text selection feature will be implemented with minimal performance impact

### Backend Scalability:
- FastAPI with async support handles concurrent requests efficiently
- Qdrant search is optimized for vector similarity
- Implement caching for frequently asked questions

## Implementation Notes

### Service Integration:
- All services can operate within free tiers for educational use
- Implement monitoring to track usage and alert when approaching limits
- Design graceful degradation when services are unavailable

### Content Strategy:
- Structure content with clear headers to maximize RAG effectiveness
- Use consistent terminology to improve semantic search
- Include code examples that can be referenced by the AI

## Conclusion

The research confirms that all required functionality can be implemented within free-tier service limits. The chosen technology stack (Groq + all-MiniLM-L6-v2) provides the best balance of cost, performance, and quality for an educational interactive textbook.