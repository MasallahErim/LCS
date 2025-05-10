# -*- coding: utf-8 -*-

import logging
from src.domains.comment.services.comment_repository import CommentRepository
from src.infrastructure.kafka.producer import CommentProducer
from src.application.dtos.comment_dto import CommentDTO

logger = logging.getLogger(__name__)

class ProduceCommentUseCase:
    def __init__(self, generator: CommentRepository, producer: CommentProducer):
        self.generator = generator
        self.producer = producer
        logger.debug("ProduceCommentUseCase initialized.")

    def execute(self):
        try:
            comment = self.generator.generate()
            logger.info(f"Generated comment: {comment}")
        except Exception as e:
            logger.exception("Comment generation failed.")
            raise

        try:
            dto = CommentDTO.from_entity(comment)
            self.producer.send(dto)
            logger.info(f"Sent comment to Kafka: {dto.json()}")
        except Exception as e:
            logger.exception("Failed to send comment to Kafka.")
            raise
