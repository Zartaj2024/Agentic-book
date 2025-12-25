---
id: 1
title: physical-ai-book
stage: plan
date: 2025-12-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: 2-physical-ai-book
branch: 2-physical-ai-book
user: Claude User
command: /sp.plan
labels: [plan,architecture,education,ai]
links:
  spec: specs/2-physical-ai-book/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/2-physical-ai-book/plan.md
 - specs/2-physical-ai-book/research.md
 - specs/2-physical-ai-book/data-model.md
 - specs/2-physical-ai-book/contracts/chat-api.yaml
 - specs/2-physical-ai-book/quickstart.md
 - specs/2-physical-ai-book/spec.md
tests:
 - null
---

## Prompt

Project Architecture Overview
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

06-capstone.md: Code for a simple "See object -> Plan reach -> Execute" pipeline.

Note: Ensure all Markdown files have clear headers (##) to facilitate better chunking for the RAG system later.

Phase 2: The RAG Brain (Backend & Embeddings)
Objective: Create the API that allows the book to "talk."

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

"You are a helpful teaching assistant for a robotics textbook. Answer the user's question using ONLY the context provided below. If the answer is not in the context, say 'I can only answer based on the book's content.'"

Generate: Send Context + Query to LLM (Groq/Gemini).

Log: Save interaction to Neon.

Return: Answer + Source Chapter references.

Phase 3: The AI Interface (Frontend Integration)
Objective: Integrate the Chatbot UI and "Select-to-Ask" feature into Docusaurus.

3.1 Floating Chatbot Component

Create a React component (/src/components/AIChatbot.js).

UI: A floating button (bottom-right) that expands into a chat window.

State: Manage messages array, isLoading, isOpen.

3.2 "Select-Text → Ask AI" Feature

Implement a global event listener in the Docusaurus layout (Layout.js wrapper).

Logic:

Detect mouseup event.

Check if window.getSelection().toString().length > 0.

Calculate coordinates of selection.

Render a small "Ask AI" tooltip button near the selection.

On click: Open Chatbot and auto-populate the input with: "Explain this: [Selected Text]".

3.3 Swizzle (Customization)

Wrap the main Docusaurus <Layout> to inject the Chatbot and Selection providers globally so they work on every page.

Phase 4: Deployment & Operations
Objective: Go live with zero cost.

## Response snapshot

Created a comprehensive implementation plan for the Physical AI Book project including:

1. Technical context with architecture overview
2. Research document addressing key technology decisions (LLM provider: Groq, Embedding model: all-MiniLM-L6-v2)
3. Detailed data model for PostgreSQL and Qdrant databases
4. OpenAPI specification for the chat API
5. Implementation plan with 4 sprints covering foundation, RAG backend, AI interface, and deployment
6. Quickstart guide for local development setup

The plan addresses all phases mentioned in the user's requirements with specific implementation details, technology choices, and timelines.

## Outcome

- ✅ Impact: Created complete implementation plan for interactive AI textbook
- 🧪 Tests: No tests needed for planning documents
- 📁 Files: Created plan.md, research.md, data-model.md, chat-api.yaml, quickstart.md
- 🔁 Next prompts: Ready for task generation (/sp.tasks) and implementation
- 🧠 Reflection: Plan addresses all architectural requirements with free-tier constraints

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Generate tasks from the plan