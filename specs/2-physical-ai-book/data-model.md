# Data Model: Physical AI Book

**Feature**: Physical AI Book (2-physical-ai-book)
**Created**: 2025-12-10
**Status**: Draft

## Overview

This document defines the data models for the Physical AI Book system, including database schemas and data structures used across the frontend, backend, and vector database.

## Database Schema (Neon Postgres)

### chat_history table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier for each interaction |
| user_query | TEXT | NOT NULL | The user's original query |
| bot_response | TEXT | NOT NULL | The AI's response to the query |
| timestamp | TIMESTAMP | DEFAULT NOW() | When the interaction occurred |
| context_used | JSONB | | The source chunks used to generate the response |
| session_id | UUID | | Identifier to group related interactions |

**Indexes**:
- `idx_timestamp`: ON (timestamp) - for time-based queries
- `idx_session_id`: ON (session_id) - for session-based analytics

## Vector Database Schema (Qdrant)

### Collection: textbook_knowledge

**Vector Configuration**:
- Size: 384 (all-MiniLM-L6-v2 embedding dimensions)
- Distance: Cosine

**Payload Structure**:

| Field | Type | Description |
|-------|------|-------------|
| chunk_id | string | Unique identifier for the text chunk |
| content | string | The actual text content of the chunk |
| chapter | string | The chapter identifier (e.g., "01-intro-physical-ai") |
| headers | json | The headers in this chunk's section for context |
| source_file | string | The original markdown file path |
| position | integer | The position of this chunk in the original document |

## Frontend Data Structures

### Chat Message Object

```typescript
interface ChatMessage {
  id: string;           // UUID for the message
  content: string;      // The message text
  role: 'user' | 'bot'; // Who sent the message
  timestamp: Date;      // When the message was sent
  sources?: string[];   // Chapter references (for bot responses)
}
```

### Chapter Metadata

```typescript
interface ChapterMetadata {
  id: string;           // Chapter ID (e.g., "01-intro-physical-ai")
  title: string;        // Display title
  position: number;     // Chapter number in sequence
  wordCount: number;    // Estimated word count
  estimatedReadingTime: number; // In minutes
}
```

## API Data Contracts

### Chat Request

```json
{
  "query": "string, the user's question",
  "session_id": "string, optional session identifier"
}
```

### Chat Response

```json
{
  "response": "string, the AI's answer",
  "sources": ["string array of chapter references"],
  "session_id": "string, session identifier"
}
```

### Ingestion Response

```json
{
  "chunks_processed": "number of text chunks ingested",
  "status": "string, success or error message"
}
```

## Relationships

1. **Chat History to Sessions**: Multiple chat interactions belong to a single session (session_id)
2. **Vector Chunks to Chapters**: Multiple text chunks belong to a single chapter (chapter field)
3. **Frontend Messages to Sessions**: Multiple messages make up a conversation session

## Validation Rules

### Chat History
- user_query must be 1-2000 characters
- bot_response must be 1-10000 characters
- timestamp cannot be in the future
- session_id should follow UUID format

### Vector Payload
- content must be 100-1000 characters (for optimal chunking)
- chapter must match existing chapter IDs
- chunk_id must be unique within the collection

### Frontend Objects
- Chat messages must have valid role values ('user' or 'bot')
- Timestamps must be in ISO 8601 format
- Chapter IDs must follow the pattern "NN-chapter-name"

## State Transitions (if applicable)

### Chat Session States
1. **Created**: Session initiated when first message is sent
2. **Active**: Session has ongoing conversation (last message < 30 min ago)
3. **Inactive**: Session has no recent activity (last message >= 30 min ago)
4. **Archived**: Session moved to archive after 30 days of inactivity

## Data Flow

1. **Content Ingestion**: Markdown files → Text chunks → Embeddings → Qdrant vectors
2. **Query Processing**: User query → Embedding → Vector search → Context retrieval → LLM response → Database logging
3. **Frontend Display**: Chat history → Session reconstruction → Message rendering