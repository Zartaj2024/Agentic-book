# Feature Specification: Physical AI Book

**Feature Branch**: `2-physical-ai-book`
**Created**: 2025-12-10
**Status**: Draft
**Input**: User description: "Project Architecture Overview
Frontend (Host): Docusaurus (Static Site Generator) hosted on GitHub Pages.

Backend (Brain): FastAPI (Python) hosted on a free-tier PaaS (e.g., Render or Railway).

Vector Database (Memory): Qdrant Cloud (Free Tier) for storing book embeddings.

Database (Logs/History): Neon (Serverless Postgres) for chat logs/analytics.

LLM (Intelligence): Groq or Gemini API (Free Tier) for fast, low-latency inference.

Embeddings: all-MiniLM-L6-v2 (Local/CPU-friendly) or OpenAI text-embedding-3-small (Low cost).

Phase 1: Foundation & Content (The Textbook)
Objective: Build the static Docusaurus site and populate it with the 6 core chapters.

1.1 Repository Setup

Initialize a Monorepo structure:

Plaintext

/physical-ai-book
├── /docs-site       # Docusaurus Frontend
├── /backend         # FastAPI + RAG Engine
├── /scripts         # Ingestion scripts
└── README.md
1.2 Docusaurus Configuration

Theme: preset-classic (Minimalist, Clean).

Config: Enable auto-sidebar to automatically generate navigation based on file structure.

Plugins: docusaurus-lunr-search (for simple offline search) or Algolia (free tier).

1.3 Content Creation (Markdown/MDX) Create the following files in /docs:

01-intro-physical-ai.md: Definition, Embodyment hypothesis, Moravec's paradox.

02-humanoid-basics.md: Kinematics, DOF (Degrees of Freedom), Actuators vs. Muscles.

03-ros2-fundamentals.md: Nodes, Topics, Services, Actions, The Graph.

04-digital-twins.md: URDF, Gazebo vs. Isaac Sim setup.

05-vla-systems.md: Vision-Language-Action models (RT-2, PaLM-E concepts).

06-capstone.md: Code for a simple \"See object -> Plan reach -> Execute\" pipeline.

Note: Ensure all Markdown files have clear headers (##) to facilitate better chunking for the RAG system later.

Phase 2: The RAG Brain (Backend & Embeddings)
Objective: Create the API that allows the book to \"talk.\"

2.1 Vector Database Setup (Qdrant)

Create a Qdrant Cloud Free Tier cluster.

Define Collection: textbook_knowledge.

Vector Config: 384 dimensions (if using all-MiniLM-L6-v2) or 1536 (if OpenAI).

2.2 Database Setup (Neon)

Create a Neon Postgres instance.

Table chat_history: id, user_query, bot_response, timestamp, context_used.

2.3 The Ingestion Pipeline (Python Script) Create a script ingest.py:

Parse: Read all .md files from /docs.

Clean: Remove Markdown syntax/images for pure text processing.

Chunk: Split text into chunks of 500 characters with 50 character overlap.

Embed: Generate vectors using sentence-transformers.

Upsert: Upload vectors + payload (text content + chapter source) to Qdrant.

2.4 FastAPI Backend Development

Endpoint: POST /chat

Logic:

Receive user query.

Embed query.

Search Qdrant: Retrieve top 3 matching chunks.

System Prompt:

\"You are a helpful teaching assistant for a robotics textbook. Answer the user's question using ONLY the context provided below. If the answer is not in the context, say 'I can only answer based on the book's content.'\"

Generate: Send Context + Query to LLM (Groq/Gemini).

Log: Save interaction to Neon.

Return: Answer + Source Chapter references.

Phase 3: The AI Interface (Frontend Integration)
Objective: Integrate the Chatbot UI and \"Select-to-Ask\" feature into Docusaurus.

3.1 Floating Chatbot Component

Create a React component (/src/components/AIChatbot.js).

UI: A floating button (bottom-right) that expands into a chat window.

State: Manage messages array, isLoading, isOpen.

3.2 \"Select-Text → Ask AI\" Feature

Implement a global event listener in the Docusaurus layout (Layout.js wrapper).

Logic:

Detect mouseup event.

Check if window.getSelection().toString().length > 0.

Calculate coordinates of selection.

Render a small \"Ask AI\" tooltip button near the selection.

On click: Open Chatbot and auto-populate the input with: \"Explain this: [Selected Text]\".

3.3 Swizzle (Customization)

Wrap the main Docusaurus <Layout> to inject the Chatbot and Selection providers globally so they work on every page.

Phase 4: Deployment & Operations
Objective: Go live with zero cost."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Access Interactive Robotics Textbook (Priority: P1)

As a student learning robotics and AI, I want to access an interactive textbook with a chatbot assistant so that I can learn complex concepts through both reading and asking questions to an AI tutor.

**Why this priority**: This is the core value proposition - providing an interactive learning experience that combines traditional textbook content with AI-powered assistance.

**Independent Test**: Can be fully tested by accessing the deployed Docusaurus site and verifying that the textbook content is readable and the chatbot is functional.

**Acceptance Scenarios**:

1. **Given** I am on the textbook website, **When** I navigate through the content, **Then** I can read all 6 core chapters with clear formatting
2. **Given** I have a question about the content, **When** I use the chatbot, **Then** I receive helpful responses based on the textbook content

---

### User Story 2 - Create Interactive Learning Content (Priority: P1)

As an educator or content creator, I want to create structured textbook content with 6 core chapters so that students can learn robotics and AI concepts systematically.

**Why this priority**: The content foundation is essential for everything else - without quality content, the AI features have no value.

**Independent Test**: Can be fully tested by creating the 6 specified chapters and verifying they contain the required topics with clear explanations.

**Acceptance Scenarios**:

1. **Given** the textbook structure, **When** I create the content, **Then** all 6 chapters (Intro to Physical AI, Humanoid Basics, ROS2 Fundamentals, Digital Twins, VLA Systems, Capstone) are complete
2. **Given** the content requirements, **When** I format the chapters, **Then** they include proper headers and structure for RAG system chunking

---

### User Story 3 - Query Textbook Content via AI (Priority: P2)

As a learner, I want to ask questions about specific textbook content and get accurate responses so that I can clarify concepts I don't understand.

**Why this priority**: This transforms a static textbook into an interactive learning tool, providing immediate help when students encounter difficulties.

**Independent Test**: Can be fully tested by asking various questions about the textbook content and verifying the AI provides accurate responses based only on the provided context.

**Acceptance Scenarios**:

1. **Given** I have a question about textbook content, **When** I ask the AI chatbot, **Then** it responds with information from the relevant chapters
2. **Given** my question is outside the textbook scope, **When** I ask the AI chatbot, **Then** it responds that it can only answer based on the book's content

---

### User Story 4 - Use Context-Specific AI Help (Priority: P2)

As a student reading the textbook, I want to select text and ask the AI about it directly so that I can get immediate clarification on specific concepts.

**Why this priority**: This provides a seamless learning experience where students can get help exactly where they need it without having to rephrase content.

**Independent Test**: Can be fully tested by selecting text on a page and using the \"Ask AI\" feature to get context-specific responses.

**Acceptance Scenarios**:

1. **Given** I have selected text in the textbook, **When** I click the \"Ask AI\" tooltip, **Then** the chatbot opens with the selected text pre-populated
2. **Given** I've selected text, **When** I use the select-to-ask feature, **Then** the AI provides explanations specifically about that content

---

### User Story 5 - Access Content Offline and Search (Priority: P3)

As a student with intermittent internet access, I want basic search functionality and offline-readable content so that I can continue learning even when connectivity is poor.

**Why this priority**: Ensures the textbook remains accessible and useful in various learning environments, especially important for educational content.

**Independent Test**: Can be fully tested by using the search functionality and verifying content loads properly for offline access.

**Acceptance Scenarios**:

1. **Given** I'm on the textbook site, **When** I use the search feature, **Then** I can find relevant content across chapters
2. **Given** the site is loaded, **When** I navigate without internet, **Then** the core content remains accessible

---

### Edge Cases

- What happens when the LLM API is temporarily unavailable?
- How does the system handle extremely long or complex queries?
- What if the selected text is too long to fit in a query?
- How does the system handle simultaneous users during peak usage?
- What happens when the vector database is temporarily unavailable?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST host the frontend using Docusaurus on GitHub Pages
- **FR-002**: System MUST implement the backend using FastAPI and host it on a free-tier PaaS (Render or Railway)
- **FR-003**: System MUST store book embeddings in a Qdrant Cloud free tier vector database
- **FR-004**: System MUST log chat interactions in a Neon (Serverless Postgres) database
- **FR-005**: System MUST use Groq or Gemini API for LLM inference with free tier limits
- **FR-006**: System MUST implement RAG (Retrieval Augmented Generation) using embeddings from all-MiniLM-L6-v2 or OpenAI text-embedding-3-small
- **FR-007**: System MUST create 6 core textbook chapters: Intro to Physical AI, Humanoid Basics, ROS2 Fundamentals, Digital Twins, VLA Systems, and Capstone
- **FR-008**: Content MUST be structured in Markdown/MDX with clear headers to facilitate RAG chunking
- **FR-009**: System MUST implement a chat endpoint that receives queries, embeds them, searches Qdrant for top 3 matching chunks, and generates responses using the LLM
- **FR-010**: System MUST include a floating chatbot component with UI that expands from a bottom-right button
- **FR-011**: System MUST implement \"Select-Text → Ask AI\" functionality that shows a tooltip when text is selected
- **FR-012**: System MUST use Docusaurus swizzling to inject global chatbot and selection functionality
- **FR-013**: The system MUST implement an ingestion pipeline that parses Markdown files, cleans content, chunks it with 500-character chunks and 50-character overlap, embeds, and uploads to Qdrant
- **FR-014**: System MUST return source chapter references with each AI response
- **FR-015**: The capstone chapter MUST include code for a \"See object -> Plan reach -> Execute\" pipeline

### Key Entities *(include if feature involves data)*

- **Textbook Content**: Educational material organized into 6 chapters, stored as Markdown files with proper headers and structure
- **Chat Interaction**: Record of user queries, AI responses, timestamps, and context used, stored in Neon Postgres database
- **Vector Embedding**: Numerical representations of textbook content chunks stored in Qdrant for semantic search
- **User Session**: Temporary state for chat interactions including message history and loading status

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The Docusaurus-based textbook site is successfully deployed to GitHub Pages with all 6 core chapters
- **SC-002**: The FastAPI backend is deployed to a free-tier PaaS and successfully handles chat queries
- **SC-003**: The Qdrant vector database contains properly embedded textbook content accessible for semantic search
- **SC-004**: Students can ask questions about textbook content and receive accurate responses based only on the provided context
- **SC-005**: The \"Select-Text → Ask AI\" feature works seamlessly, allowing students to get help on specific content
- **SC-006**: The system stays within free-tier usage limits for all services (Qdrant, Neon, LLM API)
- **SC-007**: All 6 textbook chapters are complete with proper structure and content as specified
- **SC-008**: The system can handle multiple concurrent users without performance degradation