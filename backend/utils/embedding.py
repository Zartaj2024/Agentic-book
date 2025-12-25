from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
from typing import List, Union

load_dotenv()

class EmbeddingModel:
    def __init__(self):
        # Get embedding model from environment or default
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """Encode text(s) into embeddings"""
        return self.model.encode(texts).tolist()

    def encode_single(self, text: str) -> List[float]:
        """Encode a single text into an embedding"""
        return self.model.encode([text])[0].tolist()

    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embeddings"""
        # Create a sample embedding to determine dimension
        sample_embedding = self.model.encode(["sample text"])
        return sample_embedding.shape[1]

# Global embedding model instance
embedding_model = EmbeddingModel()