
from abc import ABC, abstractmethod
from typing import List
from src.domains.comment.entities.comment import Comment

class CommentRepository(ABC):

    @abstractmethod
    def save(self, comment: Comment) -> None:
        ...

    @abstractmethod
    def list_all(self) -> List[Comment]:
        ...

    @abstractmethod
    def list_by_sentiment(self, sentiment: str) -> List[Comment]:
        ...