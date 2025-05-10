# src/infrastructure/db/comment_repository.py


import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from src.domains.comment.services.comment_repository import CommentRepository
from src.domains.comment.entities.comment import Comment
from config import settings

logger = logging.getLogger(__name__)

class PostgresCommentRepository(CommentRepository):
    def __init__(self):
        try:
            self.conn = psycopg2.connect(settings.postgres_url)
            logger.debug("PostgreSQL connection established.")
            self._ensure_table()
        except Exception:
            logger.exception("Failed to connect to PostgreSQL.")
            raise

    def _ensure_table(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS comments (
                        comment_id UUID PRIMARY KEY,
                        text TEXT NOT NULL,
                        timestamp TIMESTAMP NOT NULL,
                        sentiment TEXT
                    );
                """)
                self.conn.commit()
                logger.debug("Ensured that 'comments' table exists.")
        except Exception:
            logger.exception("Failed to ensure 'comments' table exists.")
            raise

    def save(self, comment: Comment) -> None:
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO comments (comment_id, text, timestamp, sentiment) VALUES (%s, %s, %s, %s) "
                    "ON CONFLICT (comment_id) DO NOTHING;",
                    (str(comment.comment_id), comment.text, comment.timestamp, comment.sentiment)
                )
                self.conn.commit()
                logger.info(f"Comment saved to DB: id={str(comment.comment_id)}")
        except Exception:
            logger.exception(f"Failed to save comment: id={str(comment.comment_id)}")
            raise

    def list_all(self) -> list[Comment]:
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT comment_id, text, timestamp, sentiment FROM comments;")
                rows = cur.fetchall()
            logger.info(f"Retrieved all comments from DB: count={len(rows)}")
            return [
                Comment(row['comment_id'], row['text'], row['timestamp'], row['sentiment'])
                for row in rows
            ]
        except Exception:
            logger.exception("Failed to list all comments.")
            raise

    def list_by_sentiment(self, sentiment: str) -> list[Comment]:
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    "SELECT comment_id, text, timestamp, sentiment FROM comments WHERE sentiment = %s;",
                    (sentiment,)
                )
                rows = cur.fetchall()
            logger.info(f"Comments fetched by sentiment='{sentiment}': count={len(rows)}")
            return [
                Comment(row['comment_id'], row['text'], row['timestamp'], row['sentiment'])
                for row in rows
            ]
        except Exception:
            logger.exception(f"Failed to fetch comments by sentiment='{sentiment}'")
            raise
