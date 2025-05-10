# -*- coding: utf-8 -*-
# src/application/dtos/processed_comment_dto.py

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from src.domains.comment.entities.comment import Comment as CommentEntity

class ProcessedCommentDTO(BaseModel):
    commentId: UUID
    text: str
    timestamp: datetime
    sentiment: str

    @classmethod
    def from_entity(cls, entity: CommentEntity) -> "ProcessedCommentDTO":
        return cls(
            commentId=entity.comment_id,
            text=entity.text,
            timestamp=entity.timestamp,
            sentiment=entity.sentiment
        )
