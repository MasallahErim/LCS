# -*- coding: utf-8 -*-
# src/application/use_cases/analyze_sentiment.py

import time
import grpc
import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
import pybreaker

from src.infrastructure.grpc.sentiment_client import SentimentClient
from src.infrastructure.cache.comment_cache import CommentCache
from config import settings

logger = logging.getLogger(__name__)

breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=30,
)

class AnalyzeSentimentUseCase:
    def __init__(self, cache: CommentCache, grpc_host: str = settings.grpc_host, grpc_port: int = settings.grpc_port):
        self.cache = cache
        self.client = SentimentClient(host=grpc_host, port=grpc_port)
        logger.debug("AnalyzeSentimentUseCase initialized.")

    @retry(
        retry=retry_if_exception_type(grpc.RpcError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.1, min=0.1, max=1)
    )
    @breaker
    def _call_grpc(self, text: str) -> str:
        logger.debug(f"Calling gRPC service for sentiment analysis.")
        return self.client.analyze(text)

    def execute(self, text: str) -> str:
        if (cached := self.cache.get_sentiment(text)) is not None:
            logger.info(f"Cache hit for sentiment: '{cached}' → text='{text[:20]}…'")
            return cached

        try:
            sentiment = self._call_grpc(text)
            logger.info(f"Sentiment via gRPC: '{sentiment}' → text='{text[:20]}…'")
        except grpc.RpcError as e:
            logger.warning(f"gRPC failed for text='{text[:20]}…', falling back. Error: {str(e)}")
            sentiment = self.cache.get_sentiment(text) or "NEUTRAL"

        self.cache.set_sentiment(text, sentiment)
        logger.debug(f"Sentiment cached for text='{text[:20]}…' → '{sentiment}'")
        return sentiment
