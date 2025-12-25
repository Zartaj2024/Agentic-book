#!/usr/bin/env python3
"""
Script to ingest textbook content into Qdrant vector database
"""
import asyncio
import os
import sys
import uuid
from pathlib import Path
from typing import List, Dict, Any
import logging

# Add the backend directory to the path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from utils.embedding import embedding_model
from utils.vector_db import vector_db
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def read_text_file(file_path: Path) -> str:
    """Read content from a text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info(f"Successfully read file: {file_path}")
        return content
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return ""


def read_pdf_file(file_path: Path) -> str:
    """Read content from a PDF file"""
    try:
        import PyPDF2
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        logger.info(f"Successfully read PDF file: {file_path}")
        return text
    except ImportError:
        logger.error("PyPDF2 not installed. Install with: pip install PyPDF2")
        return ""
    except Exception as e:
        logger.error(f"Error reading PDF file {file_path}: {e}")
        return ""


def read_docx_file(file_path: Path) -> str:
    """Read content from a DOCX file"""
    try:
        from docx import Document
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        logger.info(f"Successfully read DOCX file: {file_path}")
        return text
    except ImportError:
        logger.error("python-docx not installed. Install with: pip install python-docx")
        return ""
    except Exception as e:
        logger.error(f"Error reading DOCX file {file_path}: {e}")
        return ""


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks"""
    if not text:
        return []
    
    words = text.split()
    chunks = []
    
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        
        # If chunk is smaller than chunk_size, we're at the end
        if len(words[start:end]) < chunk_size:
            chunks.append(chunk)
            break
        
        chunks.append(chunk)
        
        # Move start by chunk_size minus overlap
        start = end - overlap
    
    logger.info(f"Text split into {len(chunks)} chunks")
    return chunks


async def ingest_file(file_path: Path, chapter_name: str = None) -> int:
    """Ingest a single file into the vector database"""
    if not file_path.exists():
        logger.error(f"File does not exist: {file_path}")
        return 0
    
    # Determine file type and read content
    file_ext = file_path.suffix.lower()
    content = ""
    
    if file_ext == '.txt':
        content = read_text_file(file_path)
    elif file_ext == '.pdf':
        content = read_pdf_file(file_path)
    elif file_ext == '.docx':
        content = read_docx_file(file_path)
    else:
        logger.error(f"Unsupported file type: {file_ext}")
        logger.info("Supported file types: .txt, .pdf, .docx")
        return 0
    
    if not content.strip():
        logger.warning(f"No content found in file: {file_path}")
        return 0
    
    # Use filename as chapter name if not provided
    if not chapter_name:
        chapter_name = file_path.stem
    
    # Chunk the content
    chunks = chunk_text(content, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    
    # Process and store each chunk
    points = []
    for i, chunk in enumerate(chunks):
        if chunk.strip():  # Only process non-empty chunks
            try:
                # Generate embedding for the chunk
                vector = embedding_model.encode_single(chunk)
                
                # Create a point for Qdrant
                point = {
                    "id": str(uuid.uuid4()),
                    "vector": vector,
                    "payload": {
                        "content": chunk,
                        "chapter": chapter_name,
                        "source_file": str(file_path),
                        "chunk_index": i,
                        "source_type": file_ext[1:]  # Remove the dot
                    }
                }
                points.append(point)
            except Exception as e:
                logger.error(f"Error processing chunk {i} from {file_path}: {e}")
    
    if points:
        try:
            # Upsert vectors to Qdrant
            await vector_db.upsert_vectors(points)
            logger.info(f"Successfully ingested {len(points)} chunks from {file_path}")
            return len(points)
        except Exception as e:
            logger.error(f"Error upserting vectors for {file_path}: {e}")
            return 0
    else:
        logger.warning(f"No valid chunks to ingest from {file_path}")
        return 0


async def ingest_directory(directory_path: Path, recursive: bool = True) -> int:
    """Ingest all supported files from a directory"""
    if not directory_path.exists():
        logger.error(f"Directory does not exist: {directory_path}")
        return 0
    
    if not directory_path.is_dir():
        logger.error(f"Path is not a directory: {directory_path}")
        return 0
    
    # Find all supported files
    supported_extensions = ['.txt', '.pdf', '.docx']
    files = []
    
    if recursive:
        for ext in supported_extensions:
            files.extend(directory_path.rglob(f"*{ext}"))
    else:
        for ext in supported_extensions:
            files.extend(directory_path.glob(f"*{ext}"))
    
    if not files:
        logger.warning(f"No supported files found in {directory_path}")
        logger.info("Supported file types: .txt, .pdf, .docx")
        return 0
    
    logger.info(f"Found {len(files)} files to process")
    
    total_chunks = 0
    for file_path in files:
        logger.info(f"Processing file: {file_path}")
        chunks_processed = await ingest_file(file_path)
        total_chunks += chunks_processed
    
    logger.info(f"Total chunks ingested: {total_chunks}")
    return total_chunks


async def main():
    """Main function to run the ingestion script"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest textbook content into Qdrant vector database")
    parser.add_argument("input", help="Path to input file or directory")
    parser.add_argument("--chapter", "-c", help="Chapter name for the content (for single files)")
    parser.add_argument("--recursive", "-r", action="store_true", help="Process directories recursively")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    # Validate configuration
    if not config.QDRANT_URL:
        logger.error("QDRANT_URL environment variable is not set")
        sys.exit(1)
    
    if not config.LLM_API_KEY:
        logger.error("LLM_API_KEY environment variable is not set")
        sys.exit(1)
    
    # Initialize the vector database
    try:
        vector_db.create_collection()
        logger.info("Connected to Qdrant and verified collection exists")
    except Exception as e:
        logger.error(f"Error connecting to Qdrant: {e}")
        sys.exit(1)
    
    # Process the input
    if input_path.is_file():
        # Process single file
        chunks_processed = await ingest_file(input_path, args.chapter)
    elif input_path.is_dir():
        # Process directory
        chunks_processed = await ingest_directory(input_path, args.recursive)
    else:
        logger.error(f"Input path does not exist: {input_path}")
        sys.exit(1)
    
    logger.info(f"Ingestion completed. Processed {chunks_processed} chunks.")


if __name__ == "__main__":
    asyncio.run(main())