from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging
from typing import Callable, Awaitable

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorHandler:
    """
    Error handling middleware for the Physical AI Book API
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        try:
            await self.app(scope, receive, send)
        except HTTPException as e:
            logger.error(f"HTTP Exception: {e.status_code} - {e.detail}")
            response = JSONResponse(
                status_code=e.status_code,
                content={
                    "error": e.detail,
                    "code": e.status_code
                }
            )
            await response(scope, receive, send)
        except Exception as e:
            logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)
            response = JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "code": 500,
                    "details": str(e) if __name__ == "__main__" else "An unexpected error occurred"
                }
            )
            await response(scope, receive, send)

# Alternative approach using FastAPI's built-in exception handlers
def add_exception_handlers(app):
    """
    Add exception handlers to the FastAPI app
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "code": exc.status_code
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        logger.error(f"General Exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "code": 500,
                "details": str(exc) if __name__ == "__main__" else "An unexpected error occurred"
            }
        )