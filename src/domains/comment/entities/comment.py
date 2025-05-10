# src/domains/comment/entities/comment.py

import uuid
from datetime import datetime
from typing import Optional

class Comment:
    def __init__(
        self,
        comment_id: uuid.UUID,
        text: str,
        timestamp: datetime,
        sentiment: Optional[str] = None
    ):
        self.comment_id = comment_id
        self.text = text
        self.timestamp = timestamp
        self.sentiment = sentiment

    def set_sentiment(self, sentiment: str):
        self.sentiment = sentiment
