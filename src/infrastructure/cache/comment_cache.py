# -*- coding: utf-8 -*-
# src/infrastructure/cache/comment_cache.py

import redis
import time
from typing import Optional
from uuid import UUID
from config import settings


class CommentCache:
    def __init__(self, redis_url: str = settings.redis_url):
        print(f"[Cache] Using redis_url = {redis_url}")
        for attempt in range(10):
            try:
                self._redis = redis.from_url(redis_url)
                if self._redis.ping():
                    print(f"[Cache] Connected to Redis (attempt {attempt+1})")
                    break
            except redis.ConnectionError:
                print(f"[Cache] Redis not ready at {redis_url}, retrying…")
                time.sleep(2)
        else:
            raise RuntimeError(f"Cannot connect to Redis at {redis_url}")

    def get_sentiment(self, text: str) -> Optional[str]:
        key = f"sentiment:{text}"
        val = self._redis.get(key)
        return val.decode() if val is not None else None

    def set_sentiment(self, text: str, sentiment: str, ttl_seconds: int = 3600) -> None:
        key = f"sentiment:{text}"
        self._redis.setex(key, ttl_seconds, sentiment)

    def is_processed(self, comment_id: UUID) -> bool:
        key = f"processed:{comment_id}"
        return self._redis.exists(key) == 1

    def mark_processed(self, comment_id: UUID, ttl_seconds: int = 86400) -> None:
        key = f"processed:{comment_id}"
        self._redis.setex(key, ttl_seconds, "1")
