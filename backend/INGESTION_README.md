# Data Ingestion Guide

This guide explains how to ingest your textbook content into the Qdrant vector database for the Physical AI Book API.

## Prerequisites

Before running the ingestion script, ensure you have:

1. Set up your environment variables in `.env`:
   - `QDRANT_URL`: Your Qdrant database URL
   - `QDRANT_API_KEY`: Your Qdrant API key (if required)
   - `LLM_API_KEY`: Your LLM provider API key
   - `EMBEDDING_MODEL`: The embedding model to use (default: all-MiniLM-L6-v2)

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r ingestion_requirements.txt  # for PDF and DOCX support
   ```

## Supported File Formats

The ingestion script supports the following file formats:
- `.txt` - Plain text files
- `.pdf` - PDF documents
- `.docx` - Microsoft Word documents

## How to Ingest Data

### 1. Ingest a Single File

To ingest a single file:

```bash
python scripts/ingest.py path/to/your/file.txt
```

You can also specify a chapter name:

```bash
python scripts/ingest.py path/to/your/file.txt --chapter "Chapter 1: Introduction"
```

### 2. Ingest All Files in a Directory

To ingest all supported files in a directory:

```bash
python scripts/ingest.py path/to/your/directory
```

By default, this will process subdirectories recursively. To disable recursion:

```bash
python scripts/ingest.py path/to/your/directory --recursive
```

### 3. Example Commands

```bash
# Ingest a single text file
python scripts/ingest.py sample_robotics_chapter.txt --chapter "Robotics Introduction"

# Ingest all files in a directory
python scripts/ingest.py ./textbook_content

# Ingest with specific chapter names
python scripts/ingest.py ./chapters/chapter1.txt --chapter "Chapter 1: Basics of Robotics"
```

## Configuration

The ingestion process uses the following configuration from `config.py`:

- `CHUNK_SIZE`: Size of text chunks (default: 500 words)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 50 words)
- `EMBEDDING_MODEL`: Model used for creating embeddings

You can adjust these values in your `.env` file:

```env
CHUNK_SIZE=500
CHUNK_OVERLAP=50
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## How It Works

1. The script reads your document and splits it into manageable chunks
2. Each chunk is converted to a vector embedding using the specified model
3. The embeddings and associated metadata are stored in Qdrant
4. When users query the system, relevant chunks are retrieved based on vector similarity

## Verification

After ingestion, you can test that your content was properly ingested by:

1. Making a query to your API that should match content from your ingested files
2. Using the monitoring endpoint to check that vector searches are working
3. Checking the Qdrant dashboard (if available) to confirm vectors were added

## Troubleshooting

- If you get "QDRANT_URL not set" error, make sure your `.env` file has the correct configuration
- For PDF ingestion issues, ensure PyPDF2 is installed: `pip install PyPDF2`
- For DOCX ingestion issues, ensure python-docx is installed: `pip install python-docx`
- If ingestion seems slow, check your embedding model and consider using a faster one for large documents