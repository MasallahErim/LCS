# # src/infrastructure/kafka/consumer.py
import json
import logging
from kafka import KafkaConsumer
from typing import Callable

logger = logging.getLogger(__name__)

class CommentConsumer:
    def __init__(
        self,
        bootstrap_servers: list[str],
        group_id: str,
        callback: Callable[[dict], any],
    ):
        self._topic = "raw-comments"
        self._callback = callback
        try:
            self._consumer = KafkaConsumer(
                self._topic,
                bootstrap_servers=bootstrap_servers,
                group_id=group_id,
                auto_offset_reset="latest",  # sadece yeni gelen mesajları dinler
                enable_auto_commit=True,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            )
            logger.debug(f"Kafka consumer initialized on topic '{self._topic}' with group_id='{group_id}'")
        except Exception:
            logger.exception("Failed to initialize Kafka consumer")
            raise

    def listen(self) -> None:
        logger.info(f"Listening for messages on topic '{self._topic}'...")
        try:
            for msg in self._consumer:
                data = msg.value 
                logger.info(f"Received message from Kafka: {self._preview(data)}")
                if self._callback:
                    try:
                        self._callback(data)
                    except Exception:
                        logger.exception("Callback function failed while processing message.")
        except Exception:
            logger.exception("Kafka consumer listen loop failed.")
            raise

    @staticmethod
    def _preview(data: dict) -> str:
        try:
            return json.dumps(data, default=str)[:100] + "..."
        except Exception:
            return "[Message preview failed]"
