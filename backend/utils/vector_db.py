from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class VectorDB:
    def __init__(self):
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if not self.qdrant_url:
            raise ValueError("QDRANT_URL environment variable is not set")

        try:
            # Initialize Qdrant client
            if self.qdrant_api_key:
                self.client = QdrantClient(
                    url=self.qdrant_url,
                    api_key=self.qdrant_api_key,
                    prefer_grpc=False
                )
            else:
                self.client = QdrantClient(url=self.qdrant_url)

            logger.info("Qdrant client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client: {e}")
            raise

        self.collection_name = "textbook_knowledge"
        self.vector_size = 384  # For all-MiniLM-L6-v2 embeddings

    def create_collection(self):
        """Create the textbook knowledge collection if it doesn't exist"""
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' already exists")
        except Exception:
            # Create collection with 384 dimensions for all-MiniLM-L6-v2
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Created collection: {self.collection_name}")

    async def upsert_vectors(self, points: List[Dict]):
        """Upsert vectors to the collection"""
        try:
            # Prepare points for upsert
            qdrant_points = []
            for point in points:
                qdrant_points.append(
                    models.PointStruct(
                        id=point["id"],
                        vector=point["vector"],
                        payload=point["payload"]
                    )
                )

            # Upsert the points
            self.client.upsert(
                collection_name=self.collection_name,
                points=qdrant_points
            )
            logger.info(f"Successfully upserted {len(qdrant_points)} vectors")
        except Exception as e:
            logger.error(f"Failed to upsert vectors: {e}")
            raise

    async def search_vectors(self, query_vector: List[float], limit: int = 3) -> List[Dict]:
        """Search for similar vectors in the collection"""
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )

            # Extract content and metadata from results
            search_results = []
            for result in results:
                search_results.append({
                    "id": result.id,
                    "content": result.payload.get("content", ""),
                    "chapter": result.payload.get("chapter", ""),
                    "source_file": result.payload.get("source_file", ""),
                    "score": result.score
                })

            logger.info(f"Search completed, found {len(search_results)} results")
            return search_results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise

    async def get_all_chunks_for_chapter(self, chapter: str) -> List[Dict]:
        """Get all chunks for a specific chapter"""
        try:
            results, _ = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="chapter",
                            match=models.MatchValue(value=chapter)
                        )
                    ]
                ),
                limit=10000  # Adjust as needed
            )

            chunks = []
            for point in results:
                chunks.append({
                    "id": point.id,
                    "content": point.payload.get("content", ""),
                    "chapter": point.payload.get("chapter", ""),
                    "source_file": point.payload.get("source_file", ""),
                    "headers": point.payload.get("headers", {})
                })

            logger.info(f"Retrieved {len(chunks)} chunks for chapter: {chapter}")
            return chunks
        except Exception as e:
            logger.error(f"Failed to get chunks for chapter {chapter}: {e}")
            raise

# Global vector database instance
vector_db = VectorDB()