# -*- coding: utf-8 -*-
import time
import logging

from src.infrastructure.comment_generation.hf_generator import HFCommentGenerator
from src.infrastructure.kafka.producer import CommentProducer
from src.application.use_cases.produce_comment import ProduceCommentUseCase
from config import settings
from src.infrastructure.logging.logger import setup_logging  

setup_logging(level="INFO", log_to_file=False)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Producer is starting...")

    try:

        
        gen = HFCommentGenerator(model_name="gpt2") 
        prod = CommentProducer(settings.kafka_bootstrap) 
        uc = ProduceCommentUseCase(generator=gen, producer=prod)
        logger.info("Producer dependencies initialized successfully.")
    except Exception:
        logger.exception("Failed to initialize producer components.")
        raise
    while True:
        try:
            uc.execute()
            logger.info("New comment generated and published.")
        except Exception:
            logger.exception("Failed to produce and send comment.")
        time.sleep(2)
        