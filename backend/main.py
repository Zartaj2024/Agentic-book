from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
from config import config

# Load environment variables
load_dotenv()

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Import routers
from routers import chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    from utils.database import db
    await db.create_pool()

    from utils.vector_db import vector_db
    vector_db.create_collection()

    yield

    # Shutdown
    await db.close_pool()

# Create the FastAPI app
app = FastAPI(
    title="Physical AI Book API",
    description="API for the Physical AI Book's RAG system",
    version="1.0.0",
    lifespan=lifespan
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/")
@limiter.limit(config.ROOT_RATE_LIMIT)  # Limit to root requests per minute per IP
def read_root(request):
    return {"message": "Physical AI Book API is running!"}

@app.get("/health")
@limiter.limit(config.HEALTH_RATE_LIMIT)  # Limit to health check requests per minute per IP
def health_check(request):
    return {"status": "healthy"}