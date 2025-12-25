import asyncpg
import os
from typing import Optional
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self.database_url = os.getenv("DATABASE_URL")

    async def create_pool(self):
        """Create a connection pool to the database"""
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable is not set")

        try:
            self.pool = await asyncpg.create_pool(
                dsn=self.database_url,
                min_size=2,
                max_size=10,
                command_timeout=60
            )
            logger.info("Database connection pool created successfully")
        except Exception as e:
            logger.error(f"Failed to create database connection pool: {e}")
            raise

    async def get_connection(self):
        """Get a connection from the pool"""
        if not self.pool:
            await self.create_pool()
        return self.pool

    async def close_pool(self):
        """Close the connection pool"""
        if self.pool:
            try:
                await self.pool.close()
                logger.info("Database connection pool closed")
            except Exception as e:
                logger.error(f"Error closing database connection pool: {e}")

    async def log_chat_interaction(self, user_query: str, bot_response: str, session_id: str, context_used: dict = None):
        """Log a chat interaction to the database"""
        if not self.pool:
            await self.create_pool()

        try:
            async with self.pool.acquire() as conn:
                query = """
                    INSERT INTO chat_history (user_query, bot_response, session_id, context_used)
                    VALUES ($1, $2, $3, $4)
                    RETURNING id, timestamp
                """
                result = await conn.fetchrow(
                    query,
                    user_query,
                    bot_response,
                    session_id,
                    context_used or {}
                )
                logger.info(f"Chat interaction logged successfully with ID: {result['id'] if result else 'unknown'}")
                return result
        except Exception as e:
            logger.error(f"Failed to log chat interaction: {e}")
            # Don't fail the entire request if logging fails
            return None

# Global database connection instance
db = DatabaseConnection()