# -*- coding: utf-8 -*-
# src/infrastructure/comment_generation/hf_generator.py

import uuid
import random
from datetime import datetime
from transformers import pipeline
from src.domains.comment_generation.services import CommentGenerator
from src.domains.comment.entities.comment import Comment

class HFCommentGenerator(CommentGenerator):

    def __init__(self, model_name: str = "gpt2", reuse_prob: float = 0.3):
        self._generator = pipeline("text-generation", model=model_name)
        self._last_text: str | None = None
        self._reuse_prob = reuse_prob

    def generate(self) -> Comment:
        if self._last_text is not None and random.random() < self._reuse_prob:
            text = self._last_text
        else:
            raw = self._generator(
                "", 
                max_length=50, 
                num_return_sequences=1, 
                truncation=True  
            )[0]["generated_text"]
            text = raw.strip()
            self._last_text = text


        comment_id = uuid.uuid4()
        timestamp = datetime.utcnow()
        return Comment(comment_id=comment_id, text=text, timestamp=timestamp)