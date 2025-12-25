# Implementation Plan: Physical AI Book

**Feature Spec**: [specs/2-physical-ai-book/spec.md](../2-physical-ai-book/spec.md)
**Created**: 2025-12-10
**Status**: Draft
**Plan Version**: 1.0

## Technical Context

The Physical AI Book is an interactive textbook that combines traditional educational content with AI-powered assistance. The architecture follows a monorepo structure with:

- **Frontend**: Docusaurus static site hosted on GitHub Pages
- **Backend**: FastAPI service for RAG functionality
- **Vector Database**: Qdrant Cloud for embeddings
- **History Database**: Neon Postgres for chat logs
- **LLM Service**: Groq or Gemini API for inference
- **Embeddings**: all-MiniLM-L6-v2 or OpenAI text-embedding-3-small

This system will provide students with an interactive learning experience where they can read textbook content and ask questions to an AI tutor that responds based on the book's content.

### Architecture Components

1. **Docusaurus Frontend**: Static site with textbook content and interactive AI features
2. **FastAPI Backend**: RAG engine that processes queries against textbook embeddings
3. **Ingestion Pipeline**: Converts Markdown content to vector embeddings
4. **Vector Storage**: Qdrant collection for semantic search
5. **Chat History**: Neon database for tracking interactions
6. **AI Interface**: React components for chatbot and text selection features

### Technology Stack

- **Frontend**: Docusaurus, React, JavaScript/TypeScript
- **Backend**: Python, FastAPI, sentence-transformers
- **Databases**: Qdrant (vector), Neon Postgres (chat logs)
- **LLM**: Groq or Google Gemini API
- **Deployment**: GitHub Pages (frontend), Render/Railway (backend)
- **DevOps**: Git, GitHub Actions (optional for CI/CD)

### Unknowns to Resolve

- [NEEDS CLARIFICATION: Which LLM API (Groq or Gemini) is preferred and why?]
- [NEEDS CLARIFICATION: Which embedding model (all-MiniLM-L6-v2 or OpenAI) is preferred?]
- [NEEDS CLARIFICATION: What are the expected concurrent user limits for the free tier setup?]

## Constitution Check

### Alignment with Project Principles

This implementation aligns with the project's educational mission by:
- Providing accessible learning materials through free-tier services
- Creating an interactive learning experience that adapts to student needs
- Using open-source technologies (Docusaurus, FastAPI) to ensure sustainability
- Implementing RAG to ensure AI responses are grounded in textbook content

### Risk Assessment

- **Service Limits**: Free-tier services may have usage limits that could impact functionality
- **Content Quality**: AI responses depend on the quality and completeness of textbook content
- **User Experience**: Complex architecture with multiple services could impact performance

## Phase 0: Research & Discovery

### Research Tasks

1. **LLM Provider Comparison**: Compare Groq vs Gemini for educational use cases
   - Cost implications for expected usage
   - Response quality for educational content
   - Free tier limitations and quotas

2. **Embedding Model Selection**: Compare all-MiniLM-L6-v2 vs OpenAI embeddings
   - Performance differences for educational text
   - Cost implications for vector database
   - Quality of semantic search results

3. **Free Tier Limitations**: Research usage limits for all services
   - Qdrant Cloud free tier capabilities
   - Neon Postgres serverless limits
   - LLM API rate limits and quotas

4. **Docusaurus Integration**: Research best practices for AI component integration
   - Swizzling approach for global components
   - Performance considerations for client-side features
   - Mobile responsiveness for educational content

### Expected Outcomes

- Decision on LLM provider based on cost/performance for educational use
- Decision on embedding model based on quality/cost tradeoffs
- Understanding of service limitations to inform architecture decisions
- Clear approach for integrating AI components into Docusaurus frontend

## Phase 1: Architecture & Design

### Data Model

1. **ChatInteraction** (PostgreSQL)
   - id: UUID
   - user_query: TEXT
   - bot_response: TEXT
   - timestamp: TIMESTAMP
   - context_used: JSONB
   - session_id: UUID

2. **TextbookChunk** (Qdrant payload)
   - chunk_id: STRING
   - content: TEXT
   - chapter: STRING
   - headers: JSON
   - source_file: STRING

3. **Chapter** (Markdown files)
   - chapter_id: STRING (filename)
   - title: STRING
   - content: TEXT (Markdown)
   - prerequisites: ARRAY

### API Contracts

1. **POST /chat** (FastAPI endpoint)
   - Request: {query: string, session_id?: string}
   - Response: {response: string, sources: string[], session_id: string}
   - Error: {error: string, code: number}

2. **POST /ingest** (Admin endpoint)
   - Request: {force: boolean}
   - Response: {chunks_processed: number, status: string}
   - Error: {error: string}

### Infrastructure Design

1. **Monorepo Structure**:
   ```
   /physical-ai-book
   ├── /docs-site       # Docusaurus Frontend
   │   ├── /src
   │   │   └── /components
   │   │       └── AIChatbot.js
   │   ├── /docs
   │   │   ├── 01-intro-physical-ai.md
   │   │   ├── 02-humanoid-basics.md
   │   │   ├── 03-ros2-fundamentals.md
   │   │   ├── 04-digital-twins.md
   │   │   ├── 05-vla-systems.md
   │   │   └── 06-capstone.md
   │   └── docusaurus.config.js
   ├── /backend         # FastAPI + RAG Engine
   │   ├── main.py
   │   ├── /routers
   │   │   └── chat.py
   │   ├── /models
   │   │   └── chat.py
   │   └── /services
   │       ├── rag.py
   │       └── embedding.py
   ├── /scripts         # Ingestion scripts
   │   └── ingest.py
   ├── .env.example
   └── README.md
   ```

2. **Environment Variables**:
   - QDRANT_URL, QDRANT_API_KEY
   - DATABASE_URL (Neon)
   - LLM_API_KEY
   - EMBEDDING_MODEL

### Quickstart Guide

1. **Prerequisites**: Python 3.9+, Node.js 18+, Git
2. **Clone**: `git clone <repo>`
3. **Backend Setup**:
   - `cd backend && pip install -r requirements.txt`
   - `cp .env.example .env` and add credentials
   - `python scripts/ingest.py` to populate Qdrant
4. **Frontend Setup**:
   - `cd docs-site && npm install`
   - `npm start` for local development
5. **Deployment**:
   - Backend: Deploy to Render/Railway with environment variables
   - Frontend: Build and deploy to GitHub Pages

## Phase 2: Implementation Plan

### Sprint 1: Foundation & Content
**Duration**: 2-3 weeks

1. **Repository Setup** (Day 1)
   - Initialize monorepo structure
   - Set up basic Docusaurus site
   - Configure basic FastAPI project

2. **Docusaurus Configuration** (Day 2)
   - Configure preset-classic theme
   - Set up auto-sidebar generation
   - Add docusaurus-lunr-search plugin

3. **Content Creation** (Days 3-10)
   - Create 6 core chapter files in /docs:
     - 01-intro-physical-ai.md: Definition, Embodiment hypothesis, Moravec's paradox
     - 02-humanoid-basics.md: Kinematics, DOF, Actuators vs. Muscles
     - 03-ros2-fundamentals.md: Nodes, Topics, Services, Actions, The Graph
     - 04-digital-twins.md: URDF, Gazebo vs. Isaac Sim setup
     - 05-vla-systems.md: Vision-Language-Action models (RT-2, PaLM-E concepts)
     - 06-capstone.md: Code for "See object -> Plan reach -> Execute" pipeline
   - Ensure proper headers for RAG chunking

### Sprint 2: RAG Backend
**Duration**: 2-3 weeks

1. **Vector Database Setup** (Day 1-2)
   - Set up Qdrant Cloud free tier
   - Create textbook_knowledge collection
   - Configure vector dimensions based on embedding choice

2. **Database Setup** (Day 3)
   - Set up Neon Postgres instance
   - Create chat_history table with required fields

3. **Ingestion Pipeline** (Days 4-8)
   - Create ingest.py script
   - Implement Markdown parsing and cleaning
   - Implement text chunking (500 chars + 50 char overlap)
   - Implement embedding generation
   - Implement upsert to Qdrant with payload

4. **FastAPI Backend** (Days 9-15)
   - Implement POST /chat endpoint
   - Add query embedding logic
   - Add Qdrant search for top 3 chunks
   - Implement system prompt with context
   - Add LLM integration (Groq/Gemini)
   - Add chat logging to Neon
   - Add source chapter references

### Sprint 3: AI Interface
**Duration**: 2 weeks

1. **Floating Chatbot Component** (Days 1-5)
   - Create React component at /src/components/AIChatbot.js
   - Implement UI: floating button that expands to chat window
   - Add state management: messages, loading, open/close

2. **Text Selection Feature** (Days 6-10)
   - Implement global event listener in Docusaurus layout
   - Add selection detection logic
   - Create "Ask AI" tooltip near selection
   - Implement auto-population of chat with selected text

3. **Layout Integration** (Days 11-14)
   - Implement Docusaurus swizzling to wrap main layout
   - Inject Chatbot and Selection providers globally
   - Test functionality across all pages

### Sprint 4: Testing & Deployment
**Duration**: 1-2 weeks

1. **Integration Testing** (Days 1-5)
   - Test end-to-end functionality
   - Verify RAG accuracy
   - Test chat history logging
   - Test text selection feature

2. **Performance Testing** (Days 6-7)
   - Test with multiple concurrent users
   - Verify response times
   - Test with large text selections

3. **Deployment** (Days 8-14)
   - Deploy backend to Render/Railway
   - Deploy frontend to GitHub Pages
   - Set up environment variables
   - Verify production functionality

## Success Criteria

### Technical Success
- All 6 textbook chapters are deployed and accessible
- Chatbot responds accurately to questions about textbook content
- Text selection feature works seamlessly
- System stays within free-tier limits
- Response times are under 3 seconds for typical queries

### User Experience Success
- Students can navigate and read textbook content effectively
- AI responses are helpful and grounded in textbook content
- Interactive features enhance rather than distract from learning
- Mobile and desktop experiences are both functional

## Risks & Mitigation

### Technical Risks
- **Service Limits**: Monitor usage and implement rate limiting if needed
- **API Availability**: Implement graceful degradation when services are unavailable
- **Response Quality**: Continuously refine system prompts and content structure

### Schedule Risks
- **Dependency Delays**: Complete research phase early to inform technical decisions
- **Integration Complexity**: Implement incrementally with frequent testing
- **Free Tier Limitations**: Design with constraints in mind from the beginning