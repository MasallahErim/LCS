# src/presentation/api/routes.py

import logging
from flask import Blueprint, jsonify, request
from typing import List
from src.infrastructure.db.comment_repository import PostgresCommentRepository
from src.application.dtos.processed_comment_dto import ProcessedCommentDTO

logger = logging.getLogger(__name__)

comment_bp = Blueprint("comments", __name__)
repo = PostgresCommentRepository()

@comment_bp.route("/", methods=["GET"])
def get_comments():
    sentiment_filter = request.args.get("sentiment")
    limit = request.args.get("limit", type=int)

    logger.info(f"GET / request received. Sentiment={sentiment_filter}, Limit={limit}")

    try:
        entities = repo.list_all()
        if sentiment_filter:
            sentiment_filter = sentiment_filter.upper()
            entities = [e for e in entities if e.sentiment == sentiment_filter]
            logger.debug(f"Applied sentiment filter: {sentiment_filter} → matched {len(entities)} comments")

        limited_entities = entities[:limit] if limit else entities

        dtos: List[ProcessedCommentDTO] = [
            ProcessedCommentDTO.from_entity(e) for e in limited_entities
        ]

        logger.info(f"Returning {len(dtos)} comments to client.")
        return jsonify([dto.dict() for dto in dtos]), 200

    except Exception:
        logger.exception("Failed to fetch comments.")
        return jsonify({"error": "Internal server error"}), 500
