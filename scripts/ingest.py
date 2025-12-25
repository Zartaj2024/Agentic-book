#!/usr/bin/env python3
"""
Ingestion script for the Physical AI Book project.
Parses Markdown files, creates embeddings, and uploads to Qdrant vector database.
"""

import os
import sys
import argparse
import re
from pathlib import Path
from typing import List, Dict, Tuple
import asyncio
import hashlib

# Add backend to path to import our utilities
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.utils.vector_db import vector_db
from backend.utils.embedding import embedding_model
from backend.config import config


def extract_headers_from_markdown(content: str) -> List[str]:
    """
    Extract headers from markdown content to preserve context
    """
    headers = []
    lines = content.split('\n')
    current_h1 = ""
    current_h2 = ""

    for line in lines:
        # Match markdown headers
        h1_match = re.match(r'^#\s+(.+)', line)
        h2_match = re.match(r'^##\s+(.+)', line)
        h3_match = re.match(r'^###\s+(.+)', line)

        if h1_match:
            current_h1 = h1_match.group(1).strip()
            current_h2 = ""
        elif h2_match:
            current_h2 = h2_match.group(1).strip()

        # Store headers hierarchy
        header_context = {}
        if current_h1:
            header_context['h1'] = current_h1
        if current_h2:
            header_context['h2'] = current_h2
        if h3_match:
            header_context['h3'] = h3_match.group(1).strip()

        if header_context:
            headers.append(header_context)

    return headers


def clean_markdown_content(content: str) -> str:
    """
    Clean markdown content by removing syntax while preserving text
    """
    # Remove markdown links but keep the text: [text](url) -> text
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)

    # Remove bold and italic formatting
    content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # **text** -> text
    content = re.sub(r'\*(.*?)\*', r'\1', content)      # *text* -> text
    content = re.sub(r'__(.*?)__', r'\1', content)      # __text__ -> text
    content = re.sub(r'_(.*?)_', r'\1', content)        # _text_ -> text

    # Remove code blocks but keep the content
    content = re.sub(r'```[\s\S]*?```', '', content)    # Remove code blocks
    content = re.sub(r'`([^`]+)`', r'\1', content)      # `code` -> code

    # Remove image references
    content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', content)

    # Remove horizontal rules
    content = re.sub(r'^---+$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\*\*\*+$', '', content, flags=re.MULTILINE)

    # Normalize whitespace
    content = re.sub(r'\n\s*\n', '\n\n', content)  # Remove excessive empty lines
    content = re.sub(r'[ \t]+', ' ', content)      # Normalize spaces

    return content.strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into overlapping chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # If we're near the end, take the remaining text
        if end >= len(text):
            chunk = text[start:]
            if len(chunk) > 0:
                chunks.append(chunk)
            break

        # Find a good breaking point (try to break at sentence or paragraph)
        break_point = end
        for i in range(end, start, -1):
            if text[i] in ['.', '!', '?', '\n'] and i > start + chunk_size // 2:
                break_point = i + 1
                break

        # If we couldn't find a good break point, break at the original end
        if break_point == end:
            break_point = end

        chunk = text[start:break_point]
        chunks.append(chunk)

        # Move start based on overlap
        start = break_point - overlap if overlap < break_point else break_point

    return chunks


def get_markdown_files(docs_dir: str) -> List[Path]:
    """
    Get all markdown files from the docs directory
    """
    docs_path = Path(docs_dir)
    if not docs_path.exists():
        raise FileNotFoundError(f"Docs directory not found: {docs_dir}")

    # Find all .md files, excluding special files like README
    md_files = []
    for file_path in docs_path.rglob("*.md"):
        if file_path.name.lower() not in ["readme.md", "readme", ".readme"]:
            md_files.append(file_path)

    return sorted(md_files)


async def process_markdown_file(file_path: Path, chapter_id: str) -> List[Dict]:
    """
    Process a single markdown file and return chunks with embeddings
    """
    print(f"Processing file: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean the content
    cleaned_content = clean_markdown_content(content)

    # Extract headers for context
    headers = extract_headers_from_markdown(content)

    # Chunk the content
    chunks = chunk_text(cleaned_content, config.CHUNK_SIZE, config.CHUNK_OVERLAP)

    # Create points for Qdrant
    points = []
    for i, chunk in enumerate(chunks):
        # Create a unique ID for this chunk
        chunk_id = hashlib.md5(f"{chapter_id}_{i}_{chunk[:50]}".encode()).hexdigest()

        # Create embedding for the chunk
        embedding = embedding_model.encode_single(chunk)

        # Get relevant headers for this chunk position
        chunk_headers = headers[min(i, len(headers)-1)] if headers else {}

        point = {
            "id": chunk_id,
            "vector": embedding,
            "payload": {
                "chunk_id": chunk_id,
                "content": chunk,
                "chapter": chapter_id,
                "source_file": str(file_path),
                "headers": chunk_headers,
                "position": i
            }
        }

        points.append(point)

    print(f"Created {len(points)} chunks for {file_path}")
    return points


async def ingest_docs(docs_dir: str, force: bool = False):
    """
    Main ingestion function
    """
    print("Starting ingestion process...")

    # Initialize the vector database
    vector_db.create_collection()

    # Get all markdown files
    md_files = get_markdown_files(docs_dir)
    print(f"Found {len(md_files)} markdown files to process")

    if not md_files:
        print("No markdown files found to process")
        return

    # Collect all points to upload
    all_points = []

    for file_path in md_files:
        # Extract chapter ID from filename (e.g., "01-intro-physical-ai.md" -> "01-intro-physical-ai")
        chapter_id = file_path.stem

        # Process the file
        points = await process_markdown_file(file_path, chapter_id)
        all_points.extend(points)

    # Upload all points to Qdrant
    if all_points:
        print(f"Uploading {len(all_points)} vectors to Qdrant...")
        await vector_db.upsert_vectors(all_points)
        print(f"Successfully uploaded {len(all_points)} vectors to Qdrant")
    else:
        print("No vectors to upload")

    print("Ingestion process completed!")


def main():
    parser = argparse.ArgumentParser(description='Ingest textbook content into vector database')
    parser.add_argument('--docs-dir', type=str, default='docs-site/docs',
                       help='Directory containing markdown files (default: docs-site/docs)')
    parser.add_argument('--force', action='store_true',
                       help='Force re-ingestion of all content')

    args = parser.parse_args()

    # Verify environment variables are set
    if not config.QDRANT_URL or not config.DATABASE_URL or not config.LLM_API_KEY:
        print("Error: Required environment variables are not set")
        print("Please set QDRANT_URL, DATABASE_URL, and LLM_API_KEY")
        sys.exit(1)

    # Run the ingestion
    asyncio.run(ingest_docs(args.docs_dir, args.force))


if __name__ == "__main__":
    main()