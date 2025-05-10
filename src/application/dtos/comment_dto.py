from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CommentDTO(BaseModel):
    commentId: UUID
    text: str
    timestamp: datetime

    @classmethod
    def from_entity(cls, comment):
        return cls(
            commentId=comment.comment_id,
            text=comment.text,
            timestamp=comment.timestamp
        )
