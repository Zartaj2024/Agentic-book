from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Optional
import uuid
import asyncio
import httpx
from datetime import datetime
import os
from slowapi import Limiter
from slowapi.util import get_remote_address

from models.chat import ChatRequest, ChatResponse, IngestRequest, IngestResponse
from utils.database import db
from utils.vector_db import vector_db
from utils.embedding import embedding_model
from utils.monitoring import monitor
from config import config

# Initialize rate limiter for this router
limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

# System prompt for the AI tutor
SYSTEM_PROMPT = """You are a helpful teaching assistant for a robotics textbook. Answer the user's question using ONLY the context provided below. If the answer is not in the context, say 'I can only answer based on the book's content.'"""

async def call_llm_api(prompt: str) -> str:
    """
    Call the LLM API (OpenAI, Groq, or Gemini) to generate a response
    """
    llm_api_key = os.getenv("LLM_API_KEY")
    if not llm_api_key:
        raise HTTPException(status_code=500, detail="LLM_API_KEY is not configured in the Space settings.")

    # Determine which LLM provider to use based on configuration
    llm_provider = os.getenv("LLM_PROVIDER", "openai")  # Default to OpenAI
    temperature = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    max_tokens = int(os.getenv("LLM_MAX_TOKENS", "1000"))

    # Select model based on provider
    model_map = {
        "openai": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        "groq": os.getenv("GROQ_MODEL", "llama3-70b-8192"),
        "gemini": os.getenv("GEMINI_MODEL", "gemini-pro")
    }
    model = model_map.get(llm_provider, model_map["openai"])

    headers = {
        "Authorization": f"Bearer {llm_api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    # Using httpx for async HTTP requests
    async with httpx.AsyncClient() as client:
        try:
            # Determine the API endpoint based on the provider
            if llm_provider == "openai":
                api_url = "https://api.openai.com/v1/chat/completions"
            elif llm_provider == "groq":
                api_url = "https://api.groq.com/openai/v1/chat/completions"
            elif llm_provider == "gemini":
                # Note: Gemini has a different API format, this is for compatibility
                # For Gemini, we need to transform the payload
                gemini_payload = {
                    "contents": [{
                        "parts": [
                            {"text": f"{SYSTEM_PROMPT}\n\n{prompt}"}
                        ]
                    }],
                    "generationConfig": {
                        "temperature": temperature,
                        "maxOutputTokens": max_tokens
                    }
                }
                # Update headers for Gemini
                gemini_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={llm_api_key}"
                gemini_headers = {"Content-Type": "application/json"}
                response = await client.post(
                    gemini_api_url,
                    json=gemini_payload,
                    headers=gemini_headers,
                    timeout=30.0
                )

                if response.status_code != 200:
                    logger.error(f"Gemini API error ({response.status_code}): {response.text}")
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Gemini API returned an error: {response.text}"
                    )

                result = response.json()
                try:
                    if "candidates" in result and len(result["candidates"]) > 0:
                        if "content" in result["candidates"][0] and "parts" in result["candidates"][0]["content"]:
                            return result["candidates"][0]["content"]["parts"][0]["text"].strip()
                        else:
                            raise HTTPException(
                                status_code=500,
                                detail=f"No content found in Gemini response: {result}"
                            )
                    else:
                        raise HTTPException(
                            status_code=500,
                            detail=f"No candidates found in Gemini response: {result}"
                        )
                except (KeyError, IndexError) as e:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Unexpected response format from Gemini API: {result}, Error: {str(e)}"
                    )
            else:
                # Default to OpenAI format for unknown providers
                api_url = "https://api.openai.com/v1/chat/completions"

            # For OpenAI and Groq (which uses OpenAI-compatible format)
            if llm_provider in ["openai", "groq"] or llm_provider not in ["gemini"]:
                response = await client.post(
                    api_url,
                    json=payload,
                    headers=headers,
                    timeout=30.0
                )

                if response.status_code != 200:
                    logger.error(f"{llm_provider} API error ({response.status_code}): {response.text}")
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"{llm_provider} API returned an error: {response.text}"
                    )

                result = response.json()
                return result["choices"][0]["message"]["content"].strip()

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"LLM Provider {llm_provider} is unreachable: {str(e)}"
            )
        except KeyError as e:
            raise HTTPException(
                status_code=502,
                detail=f"Invalid response format from {llm_provider}: {str(e)}"
            )

@router.post("/chat", response_model=ChatResponse)
@limiter.limit(config.CHAT_RATE_LIMIT)  # Limit to chat requests per minute per IP
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    """
    Process a user query against the textbook content
    """
    try:
        # Track the incoming request
        monitor.track_request()

        # Generate a session ID if not provided
        session_id = chat_request.session_id or str(uuid.uuid4())

        # Embed the user query
        try:
            query_embedding = embedding_model.encode_single(chat_request.query)
        except Exception as e:
            logger.error(f"Embedding error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"AI brain failed to process text: {str(e)}")

        # Track the vector search operation
        monitor.track_vector_search()

        # Search the vector database for relevant chunks
        try:
            search_results = await vector_db.search_vectors(
                query_vector=query_embedding,
                limit=config.RAG_TOP_K
            )
        except Exception as e:
            logger.error(f"Qdrant search error: {str(e)}")
            raise HTTPException(status_code=502, detail=f"Knowledge base is unreachable: {str(e)}")

        if not search_results:
            response_text = "I couldn't find relevant content in the textbook to answer your question. Please try rephrasing or consult the textbook directly."
            sources = []
        else:
            # Build context from search results
            context_parts = []
            sources = []
            for result in search_results:
                context_parts.append(result["content"])
                if result["chapter"] not in sources:
                    sources.append(result["chapter"])

            context = "\n\n".join(context_parts)

            # Prepare the prompt for the LLM
            full_prompt = f"Context:\n{context}\n\nQuestion: {chat_request.query}\n\nAnswer:"

            # Track the LLM API call
            monitor.track_llm_call()

            # Call the LLM to generate a response
            response_text = await call_llm_api(full_prompt)

        # Log the interaction to the database
        await db.log_chat_interaction(
            user_query=chat_request.query,
            bot_response=response_text,
            session_id=session_id,
            context_used=search_results
        )

        return ChatResponse(
            response=response_text,
            sources=sources,
            session_id=session_id
        )
    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    except Exception as e:
        import traceback
        logger.error(f"Unexpected error in chat endpoint: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/ingest", response_model=IngestResponse)
@limiter.limit(config.INGEST_RATE_LIMIT)  # Limit to ingestion requests per hour per IP
async def ingest_endpoint(request: Request, ingest_request: IngestRequest):
    """
    Ingest textbook content into the vector database
    """
    # This endpoint is intentionally not implemented in the API
    # Ingestion should happen via separate scripts to prevent abuse
    raise HTTPException(
        status_code=501,
        detail="Ingestion endpoint not implemented. Use scripts/ingest.py for data ingestion."
    )


@router.get("/health")
@limiter.limit(config.HEALTH_RATE_LIMIT)  # Limit to health check requests per minute per IP
async def health_check(request: Request):
    """
    Health check endpoint
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@router.get("/monitoring/usage")
@limiter.limit(config.MONITORING_RATE_LIMIT)  # Limit monitoring endpoint usage
async def get_usage(request: Request):
    """
    Get current API usage statistics
    """
    try:
        # Track this monitoring request
        monitor.track_request()

        usage_report = monitor.get_usage_report()
        near_limits = monitor.is_near_limits()

        usage_report["near_limits"] = near_limits

        return usage_report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting usage report: {str(e)}")