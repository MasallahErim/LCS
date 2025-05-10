# src/domains/comment_generation/services/generator.py

from abc import ABC, abstractmethod
from src.domains.comment.entities.comment import Comment

class CommentGenerator(ABC):
    @abstractmethod
    def generate(self) -> Comment:
        ...
