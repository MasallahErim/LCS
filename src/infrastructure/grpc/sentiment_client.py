# -*- coding: utf-8 -*-
# src/infrastructure/grpc/sentiment_client.py
import grpc
import logging

from src.infrastructure.grpc.sentiment_pb2 import AnalyzeRequest
from src.infrastructure.grpc.sentiment_pb2_grpc import SentimentStub
from config import settings

logger = logging.getLogger(__name__)

class SentimentClient:

    def __init__(
        self,
        host: str = settings.grpc_host,    # "sentiment"
        port: int = settings.grpc_port,    # 50051
        timeout: float = 5.0,
    ):
        self._timeout = timeout
        self._target = f"{host}:{port}"
        try:
            logger.info(f"gRPC client initializing for {self._target}")
            channel = grpc.insecure_channel(self._target)
            self._stub = SentimentStub(channel)
            logger.debug("gRPC client stub created successfully.")
        except Exception as e:
            logger.exception(f"Failed to initialize gRPC client for {self._target}")
            raise

    def analyze(self, text: str) -> str:
        logger.debug(f"Sending text to sentiment service: {text[:50]}...")
        request = AnalyzeRequest(text=text)

        try:
            response = self._stub.Analyze(request, timeout=self._timeout)
            logger.info(f"Received sentiment: {response.sentiment}")
            return response.sentiment
        except grpc.RpcError as e:
            logger.exception(f"gRPC call failed to {self._target}")
            raise
