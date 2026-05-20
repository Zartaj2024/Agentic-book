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
            logger.warning("DATABASE_URL environment variable is not set. Chat history logging will be unavailable.")
            return

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
        return self.pool if self.pool else None

    async def close_pool(self):
        """Close the connection pool"""
        if self.pool:
            try:
                await self.pool.close()
                logger.info("Database connection pool closed")
            except Exception as e:
                logger.error(f"Error closing database connection pool: {e}")

    async def init_db(self):
        """Initialize the database schema if it doesn't exist"""
        if not self.pool:
            await self.create_pool()

        if not self.pool:
            logger.warning("Cannot initialize DB: Pool not available.")
            return

        try:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                    CREATE TABLE IF NOT EXISTS chat_history (
                        id SERIAL PRIMARY KEY,
                        user_query TEXT NOT NULL,
                        bot_response TEXT NOT NULL,
                        session_id TEXT NOT NULL,
                        context_used JSONB DEFAULT '{}',
                        timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                    CREATE INDEX IF NOT EXISTS idx_chat_session_id ON chat_history(session_id);
                """)
                logger.info("Database schema verified/created successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database schema: {e}")

    async def log_chat_interaction(self, user_query: str, bot_response: str, session_id: str, context_used: dict = None):
        """Log a chat interaction to the database"""
        try:
            if not self.pool:
                await self.create_pool()
                if not self.pool:
                    logger.warning("Cannot log interaction: Database pool is not initialized.")
                    return None
        except Exception as e:
            logger.error(f"Error initializing pool during logging: {e}")
            return None

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