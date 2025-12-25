from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="User query text")
    session_id: Optional[str] = Field(default=None, min_length=1, max_length=100, description="Session identifier")

class ChatResponse(BaseModel):
    response: str
    sources: List[str]
    session_id: str

class IngestRequest(BaseModel):
    force: bool = False
    chapters: Optional[List[str]] = Field(default=None, max_items=50, description="List of chapters to ingest")

class IngestResponse(BaseModel):
    chunks_processed: int
    status: str
    details: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    error: str
    code: int
    details: Optional[Dict[str, Any]] = None