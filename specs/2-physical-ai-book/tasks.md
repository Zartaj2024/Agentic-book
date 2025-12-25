# Tasks: Physical AI Book

**Feature**: Physical AI Book
**Plan**: [specs/2-physical-ai-book/plan.md](plan.md)
**Spec**: [specs/2-physical-ai-book/spec.md](spec.md)
**Created**: 2025-12-10
**Status**: Draft

## Implementation Strategy

This task list implements the Physical AI Book project following the architectural plan. The implementation follows an MVP-first approach with incremental delivery, starting with User Story 1 (interactive textbook access) as the core value proposition. Each user story phase is designed to be independently testable and deliver value.

## Dependencies

- User Story 1 (P1) can be implemented independently as the core feature
- User Story 2 (P1) content creation should be completed before other stories for functionality
- User Story 3 (P2) and 4 (P2) depend on backend infrastructure from Phase 2
- User Story 5 (P3) is independent but requires deployed frontend

## Parallel Execution Examples

- **User Story 1**: Frontend setup (T001-T010) and Backend setup (T011-T020) can run in parallel
- **User Story 2**: Content creation for each chapter can run in parallel across different files
- **User Story 3**: Chat API implementation (T040-T050) and chat history logging (T051-T060) can run in parallel
- **User Story 4**: Chatbot UI component (T061-T070) and text selection feature (T071-T080) can run in parallel

## Phase 1: Setup

### Goal
Initialize the monorepo structure and configure development environments for both frontend and backend.

- [x] T001 Create monorepo structure with /docs-site, /backend, and /scripts directories
- [x] T002 Initialize Git repository with appropriate .gitignore for Python and Node.js
- [x] T003 Set up Python virtual environment for backend development
- [x] T004 Create requirements.txt with FastAPI, uvicorn, sentence-transformers, qdrant-client, python-dotenv, psycopg2-binary
- [x] T005 Create .env.example with QDRANT_URL, QDRANT_API_KEY, DATABASE_URL, LLM_API_KEY, EMBEDDING_MODEL
- [x] T006 Initialize Node.js project in /docs-site with package.json
- [x] T007 Install Docusaurus dependencies and create basic site structure
- [x] T008 Configure basic Docusaurus settings in docusaurus.config.js
- [x] T009 Set up README.md with project overview and setup instructions
- [x] T010 Create initial project documentation files

## Phase 2: Foundational Infrastructure

### Goal
Set up the core infrastructure including vector database, chat history database, and basic API framework.

- [x] T011 [P] Create Qdrant collection 'textbook_knowledge' with 384 dimensions for all-MiniLM-L6-v2 embeddings
- [x] T012 [P] Set up Neon Postgres database with chat_history table as specified in data model
- [x] T013 [P] Implement basic FastAPI application structure in backend/main.py
- [x] T014 [P] Create database connection utilities for Neon Postgres in backend/utils/database.py
- [x] T015 [P] Create Qdrant client utilities in backend/utils/vector_db.py
- [x] T016 [P] Implement embedding utilities using sentence-transformers in backend/utils/embedding.py
- [x] T017 [P] Create environment configuration loader in backend/config.py
- [x] T018 [P] Set up basic API router structure in backend/routers/chat.py
- [x] T019 [P] Create data models for API requests/responses in backend/models/chat.py
- [x] T020 [P] Implement basic error handling middleware in backend/middleware/error_handler.py

## Phase 3: User Story 1 - Access Interactive Robotics Textbook (P1)

### Goal
Enable students to access the interactive textbook with readable content and basic chatbot functionality.

### Independent Test Criteria
- Can navigate through all 6 core chapters on the website
- Can access the chatbot interface and see it's connected to the backend

- [x] T021 [US1] Configure Docusaurus sidebar to auto-generate navigation from /docs files
- [x] T022 [US1] Set up Docusaurus preset-classic theme with minimalist clean design
- [x] T023 [US1] Install and configure docusaurus-lunr-search plugin for offline search
- [x] T024 [US1] Create basic page layout for textbook content with proper styling
- [x] T025 [US1] Implement basic floating chatbot button in bottom-right corner
- [x] T026 [US1] Create chatbot UI component that expands from the floating button
- [x] T027 [US1] Implement basic chat message display functionality
- [x] T028 [US1] Connect chatbot UI to backend API endpoint (placeholder for now)
- [x] T029 [US1] Style chatbot component with CSS consistent with textbook theme
- [x] T030 [US1] Test navigation and basic chatbot functionality locally

## Phase 4: User Story 2 - Create Interactive Learning Content (P1)

### Goal
Create the 6 core textbook chapters with proper structure for RAG system chunking.

### Independent Test Criteria
- All 6 chapters exist with proper content as specified
- Chapters have clear headers that facilitate RAG chunking

- [x] T031 [US2] Create 01-intro-physical-ai.md with content about Definition, Embodiment hypothesis, Moravec's paradox
- [x] T032 [US2] Create 02-humanoid-basics.md with content about Kinematics, DOF, Actuators vs. Muscles
- [x] T033 [US2] Create 03-ros2-fundamentals.md with content about Nodes, Topics, Services, Actions, The Graph
- [x] T034 [US2] Create 04-digital-twins.md with content about URDF, Gazebo vs. Isaac Sim setup
- [x] T035 [US2] Create 05-vla-systems.md with content about Vision-Language-Action models (RT-2, PaLM-E concepts)
- [x] T036 [US2] Create 06-capstone.md with content about "See object -> Plan reach -> Execute" pipeline code
- [x] T037 [US2] Add proper headers (##, ###) to all chapters to facilitate RAG chunking
- [x] T038 [US2] Structure content with clear sections and subsections
- [x] T039 [US2] Add code examples and diagrams where appropriate in each chapter
- [x] T040 [US2] Verify all chapters follow consistent formatting and structure

## Phase 5: User Story 3 - Query Textbook Content via AI (P2)

### Goal
Enable students to ask questions about textbook content and receive accurate AI responses based on the content.

### Independent Test Criteria
- Can ask questions about textbook content and receive relevant responses
- AI responses are grounded only in the textbook content provided

- [x] T041 [US3] Create ingestion script in scripts/ingest.py to parse Markdown files
- [x] T042 [US3] Implement content cleaning functionality to remove Markdown syntax for processing
- [x] T043 [US3] Implement text chunking with 500 characters and 50-character overlap
- [x] T044 [US3] Implement embedding generation using all-MiniLM-L6-v2 for chunks
- [x] T045 [US3] Implement upsert functionality to upload chunks to Qdrant with payload
- [x] T046 [US3] Create POST /chat endpoint in backend/routers/chat.py
- [x] T047 [US3] Implement query embedding logic in the chat endpoint
- [x] T048 [US3] Implement Qdrant search for top 3 matching chunks in the chat endpoint
- [x] T049 [US3] Implement system prompt with textbook context for LLM calls
- [x] T050 [US3] Implement response generation using Groq API with textbook context
- [x] T051 [US3] Implement chat history logging to Neon Postgres database
- [x] T052 [US3] Add source chapter references to AI responses
- [x] T053 [US3] Implement error handling for LLM API failures
- [x] T054 [US3] Test end-to-end chat functionality with textbook content

## Phase 6: User Story 4 - Use Context-Specific AI Help (P2)

### Goal
Enable students to select text and ask the AI about it directly for immediate clarification.

### Independent Test Criteria
- Can select text in the textbook and see an "Ask AI" tooltip appear
- Clicking the tooltip opens the chatbot with the selected text pre-populated

- [x] T055 [US4] Implement global mouse event listener in Docusaurus layout
- [x] T056 [US4] Create text selection detection logic in frontend
- [x] T057 [US4] Implement coordinate calculation for tooltip positioning
- [x] T058 [US4] Create "Ask AI" tooltip component that appears near selection
- [x] T059 [US4] Style tooltip component to match overall design
- [x] T060 [US4] Implement tooltip click handler to open chatbot
- [x] T061 [US4] Implement auto-population of chat input with selected text
- [x] T062 [US4] Modify chatbot to handle pre-populated queries from text selection
- [x] T063 [US4] Implement proper cleanup of event listeners to prevent memory leaks
- [x] T064 [US4] Test text selection feature across all textbook chapters
- [x] T065 [US4] Ensure tooltip works correctly on different screen sizes and devices

## Phase 7: User Story 5 - Access Content Offline and Search (P3)

### Goal
Provide basic search functionality and ensure content remains accessible in various conditions.

### Independent Test Criteria
- Can search across textbook content and find relevant results
- Core content remains accessible with minimal internet connectivity

- [x] T066 [US5] Enhance docusaurus-lunr-search configuration for better textbook content search
- [x] T067 [US5] Test search functionality across all 6 textbook chapters
- [x] T068 [US5] Optimize Docusaurus build for faster loading and better caching
- [x] T069 [US5] Implement service worker for basic offline content caching
- [x] T070 [US5] Test offline content accessibility for core textbook pages
- [x] T071 [US5] Document search and offline capabilities in user documentation

## Phase 8: Polish & Cross-Cutting Concerns

### Goal
Finalize the implementation with quality improvements, testing, and deployment preparation.

- [x] T072 Add comprehensive error handling and user-friendly error messages throughout the application
- [x] T073 Implement rate limiting for API endpoints to stay within free tier limits
- [x] T074 Add monitoring and logging for API usage to track free tier consumption
- [x] T075 Create comprehensive documentation for content creators and administrators
- [ ] T076 Implement graceful degradation when external services are unavailable
- [ ] T077 Add loading states and performance indicators to the UI
- [ ] T078 Optimize images and assets for faster loading
- [ ] T079 Test mobile responsiveness across all features
- [x] T080 Prepare deployment configuration files for Render/Railway and GitHub Pages
- [x] T081 Create deployment scripts for both backend and frontend
- [x] T082 Conduct final integration testing of all features
- [x] T083 Document any limitations due to free-tier constraints
- [x] T084 Create user onboarding documentation explaining all features