
# src/application/use_cases/process_comment.py

from src.application.use_cases.analyze_sentiment import AnalyzeSentimentUseCase
from src.infrastructure.kafka.producer import CommentProducer
from src.application.dtos.processed_comment_dto import ProcessedCommentDTO
from src.domains.comment.services.comment_repository import CommentRepository
from src.infrastructure.cache.comment_cache import CommentCache
from src.domains.comment.entities.comment import Comment as CommentEntity
from uuid import UUID

import logging
logger = logging.getLogger(__name__)

class ProcessCommentUseCase:
    def __init__(
        self,
        sentiment_uc: AnalyzeSentimentUseCase,
        processed_producer: CommentProducer,
        repository: CommentRepository,
        cache: CommentCache
    ):
        self.sentiment_uc = sentiment_uc
        self.producer = processed_producer
        self.repository = repository
        self.cache = cache
        logger.debug("ProcessCommentUseCase initialized.")

    def execute(self, raw_comment: dict) -> ProcessedCommentDTO:
        logger.info(f"Received new raw comment: {raw_comment}")

        try:
            comment_id = UUID(raw_comment["commentId"])
            text = raw_comment["text"]
            timestamp = raw_comment["timestamp"]
        except Exception as e:
            logger.exception(f"Invalid comment structure: {raw_comment}")
            raise

        if self.cache.is_processed(comment_id):
            logger.warning(f"Skipping duplicate comment_id={str(comment_id)}")
            return 

        logger.debug(f"Comment {str(comment_id)} is new and will be processed.")


        try:
            sentiment = self.sentiment_uc.execute(text)
            logger.info(f"Sentiment analysis result for comment_id={str(comment_id)}: {sentiment}")
        except Exception as e:
            logger.exception(f"Sentiment analysis failed for comment_id={str(comment_id)}")
            raise

        dto = ProcessedCommentDTO(
            commentId=comment_id,
            text=text,
            timestamp=timestamp,
            sentiment=sentiment
        )
        try:
            self.producer.send(dto)
            logger.info(f"Published comment_id={comment_id} to Kafka topic 'processed-comments'")
        except Exception as e:
            logger.exception(f"Failed to send comment_id={comment_id} to Kafka")
            raise
        try:
            entity = CommentEntity(
                comment_id=comment_id,
                text=text,
                timestamp=timestamp,
                sentiment=sentiment
            )
            self.repository.save(entity)
            logger.info(f"Saved comment_id={comment_id} to database")
        except Exception as e:
            logger.exception(f"Failed to save comment_id={comment_id} to database")
            raise
        try:
            self.cache.mark_processed(comment_id)
            logger.debug(f"Marked comment_id={comment_id} as processed in cache")
        except Exception as e:
            logger.exception(f"Failed to mark comment_id={comment_id} in cache")
            raise

        return dto
