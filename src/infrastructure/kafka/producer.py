# -*- coding: utf-8 -*-
# src/infrastructure/kafka/producer.py
import json
import logging
from kafka import KafkaProducer

logger = logging.getLogger(__name__)

class CommentProducer:

    def __init__(self, bootstrap_servers: list[str], topic: str = "raw-comments"):
        self._topic = topic
        self._producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: (
                v.json().encode("utf-8")
                if hasattr(v, "json")
                else json.dumps(v, default=str).encode("utf-8")
            )
        )
        logger.debug(f"Kafka producer initialized for topic '{self._topic}' on {bootstrap_servers}")

    def send(self, message) -> None:
        """
        message: Pydantic model (has .json()) veya dict
        """
        try:
            self._producer.send(self._topic, message)
            self._producer.flush()
            logger.info(f"Message sent to topic '{self._topic}': {self._preview(message)}")
        except Exception as e:
            logger.exception(f"Failed to send message to Kafka topic '{self._topic}'")

    @staticmethod
    def _preview(message):
        """
        Log için mesajın kısaltılmış versiyonunu döner
        """
        try:
            if hasattr(message, "json"):
                return message.json()[:100] + "..."
            return json.dumps(message, default=str)[:100] + "..."
        except Exception:
            return "[Message preview failed]"
