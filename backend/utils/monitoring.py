import logging
from datetime import datetime
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class APIMonitor:
    """
    Monitor API usage to track consumption and stay within free tier limits
    """

    def __init__(self):
        # Initialize counters for tracking usage
        self.request_count = 0
        self.llm_calls_count = 0
        self.vector_searches_count = 0
        self.current_date = datetime.now().date()

        # Load free tier limits from environment or use defaults
        self.llm_daily_limit = int(os.getenv("LLM_DAILY_LIMIT", "10000"))
        self.vector_search_daily_limit = int(os.getenv("VECTOR_SEARCH_DAILY_LIMIT", "100000"))
        self.request_daily_limit = int(os.getenv("REQUEST_DAILY_LIMIT", "100000"))

        logger.info(f"API Monitor initialized with limits - LLM: {self.llm_daily_limit}, "
                   f"Vector Search: {self.vector_search_daily_limit}, "
                   f"Requests: {self.request_daily_limit}")

    def reset_daily_counters(self):
        """Reset counters if it's a new day"""
        today = datetime.now().date()
        if today != self.current_date:
            logger.info(f"Resetting daily counters for new day: {today}")
            self.request_count = 0
            self.llm_calls_count = 0
            self.vector_searches_count = 0
            self.current_date = today

    def track_request(self):
        """Track an incoming API request"""
        self.reset_daily_counters()
        self.request_count += 1

        # Log warning if approaching limits
        if self.request_count > self.request_daily_limit * 0.8:  # 80% of limit
            logger.warning(f"Approaching request limit: {self.request_count}/{self.request_daily_limit}")

        if self.request_count >= self.request_daily_limit:
            logger.error(f"Request limit exceeded: {self.request_count}/{self.request_daily_limit}")
            raise Exception("Daily request limit exceeded")

    def track_llm_call(self):
        """Track a call to the LLM API"""
        self.reset_daily_counters()
        self.llm_calls_count += 1

        # Log warning if approaching limits
        if self.llm_calls_count > self.llm_daily_limit * 0.8:  # 80% of limit
            logger.warning(f"Approaching LLM API limit: {self.llm_calls_count}/{self.llm_daily_limit}")

        if self.llm_calls_count >= self.llm_daily_limit:
            logger.error(f"LLM API limit exceeded: {self.llm_calls_count}/{self.llm_daily_limit}")
            raise Exception("Daily LLM API limit exceeded")

    def track_vector_search(self):
        """Track a vector database search operation"""
        self.reset_daily_counters()
        self.vector_searches_count += 1

        # Log warning if approaching limits
        if self.vector_searches_count > self.vector_search_daily_limit * 0.8:  # 80% of limit
            logger.warning(f"Approaching vector search limit: {self.vector_searches_count}/{self.vector_search_daily_limit}")

        if self.vector_searches_count >= self.vector_search_daily_limit:
            logger.error(f"Vector search limit exceeded: {self.vector_searches_count}/{self.vector_search_daily_limit}")
            raise Exception("Daily vector search limit exceeded")

    def get_usage_report(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        return {
            "date": self.current_date.isoformat(),
            "request_count": self.request_count,
            "llm_calls_count": self.llm_calls_count,
            "vector_searches_count": self.vector_searches_count,
            "limits": {
                "request_daily_limit": self.request_daily_limit,
                "llm_daily_limit": self.llm_daily_limit,
                "vector_search_daily_limit": self.vector_search_daily_limit
            },
            "usage_percentages": {
                "requests": (self.request_count / self.request_daily_limit) * 100 if self.request_daily_limit > 0 else 0,
                "llm_calls": (self.llm_calls_count / self.llm_daily_limit) * 100 if self.llm_daily_limit > 0 else 0,
                "vector_searches": (self.vector_searches_count / self.vector_search_daily_limit) * 100 if self.vector_search_daily_limit > 0 else 0
            }
        }

    def is_near_limits(self) -> Dict[str, bool]:
        """Check if usage is approaching limits (above 80%)"""
        return {
            "requests": (self.request_count / self.request_daily_limit) * 100 > 80 if self.request_daily_limit > 0 else False,
            "llm_calls": (self.llm_calls_count / self.llm_daily_limit) * 100 > 80 if self.llm_daily_limit > 0 else False,
            "vector_searches": (self.vector_searches_count / self.vector_search_daily_limit) * 100 > 80 if self.vector_search_daily_limit > 0 else False
        }

# Global monitor instance
monitor = APIMonitor()