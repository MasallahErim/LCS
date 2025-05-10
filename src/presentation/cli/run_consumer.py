from src.infrastructure.kafka.consumer import CommentConsumer
from src.infrastructure.kafka.producer import CommentProducer
from src.infrastructure.db.comment_repository import PostgresCommentRepository
from src.infrastructure.cache.comment_cache import CommentCache
from src.application.use_cases.analyze_sentiment import AnalyzeSentimentUseCase
from src.application.use_cases.process_comment import ProcessCommentUseCase
from config import settings

def main():
    print(">>> CONSUMER STARTING…")
    cache = CommentCache()
    analyzer = AnalyzeSentimentUseCase(cache=cache)

    processed_producer = CommentProducer(
        bootstrap_servers=[settings.kafka_bootstrap],
        topic="processed-comments"
    )

    repo = PostgresCommentRepository()

    uc = ProcessCommentUseCase(
        sentiment_uc=analyzer,
        processed_producer=processed_producer,
        repository=repo,
        cache=cache
    )

    consumer = CommentConsumer(
        bootstrap_servers=[settings.kafka_bootstrap],
        group_id="comment-processor",
        callback=lambda raw: uc.execute(raw)
    )
    consumer.listen()
if __name__ == "__main__":
    main()
