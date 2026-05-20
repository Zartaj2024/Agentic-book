from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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
    try:
        await db.create_pool()
        await db.init_db()
    except Exception as e:
        print(f"Warning: Could not initialize database: {e}")

    from utils.vector_db import vector_db
    try:
        vector_db.create_collection()
    except Exception as e:
        print(f"Warning: Could not create vector collection: {e}")

    yield

    # Shutdown
    try:
        await db.close_pool()
    except Exception as e:
        print(f"Warning: Error during database pool shutdown: {e}")

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

@app.get("/health")
@limiter.limit(config.HEALTH_RATE_LIMIT)  # Limit to health check requests per minute per IP
def health_check(request: Request):
    return {"status": "healthy"}

# Serve frontend static files if they exist
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend-build")
if os.path.exists(frontend_path):
    app.mount("/docs", StaticFiles(directory=frontend_path, html=True), name="frontend")

    @app.get("/")
    @limiter.limit(config.ROOT_RATE_LIMIT)
    async def serve_frontend(request: Request):
        return FileResponse(os.path.join(frontend_path, "index.html"))

    # Catch-all to support Docusaurus client-side routing
    @app.get("/{full_path:path}")
    async def catch_all(request: Request, full_path: str):
        # Don't catch API routes or health check
        if full_path.startswith("api/v1") or full_path == "health":
            # Signal to FastAPI to continue looking for routes or return 404
            raise HTTPException(status_code=404, detail="Not Found")

        # Check if file exists, if not serve index.html
        local_file = os.path.join(frontend_path, full_path)
        if os.path.isfile(local_file):
            return FileResponse(local_file)
        return FileResponse(os.path.join(frontend_path, "index.html"))
else:
    @app.get("/")
    @limiter.limit(config.ROOT_RATE_LIMIT)  # Limit to root requests per minute per IP
    def read_root(request: Request):
        return {"message": "Physical AI Book API is running! (Frontend not found)"}
