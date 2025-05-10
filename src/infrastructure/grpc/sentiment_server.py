
# # src/infrastructure/grpc/sentiment_server.py

import time
import random
import logging
from concurrent import futures

import grpc
from src.infrastructure.grpc.sentiment_pb2 import AnalyzeResponse
from src.infrastructure.grpc import sentiment_pb2_grpc
from src.infrastructure.grpc.sentiment_pb2_grpc import add_SentimentServicer_to_server, SentimentServicer

_ONE_SECOND = 1.0
_RATE_LIMIT = 100            # saniyede 100 istek
_DROP_PROBABILITY = 0.1      # %10 rastgele drop

# Logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

class SentimentServicer(sentiment_pb2_grpc.SentimentServicer):
    def __init__(self):
        self._cache: dict[str, str] = {}
        self._window_start = time.time()
        self._count = 0

    def Analyze(self, request, context):
        text = request.text
        now = time.time()

        # Rate limit (fixed window)
        if now - self._window_start >= _ONE_SECOND:
            self._window_start = now
            self._count = 0
        self._count += 1
        if self._count > _RATE_LIMIT:
            logger.warning(f"Rate limit exceeded: {_RATE_LIMIT} req/s")
            context.abort(grpc.StatusCode.RESOURCE_EXHAUSTED, "Rate limit exceeded")

        # Random drop
        if random.random() < _DROP_PROBABILITY:
            logger.warning("Random drop triggered")
            context.abort(grpc.StatusCode.UNAVAILABLE, "Random drop")

        # Cache hit?
        if text in self._cache:
            sentiment = self._cache[text]
            logger.debug(f"Cache hit for text: '{text[:20]}...' → {sentiment}")
        else:
            sentiment = random.choice(["POSITIVE", "NEGATIVE", "NEUTRAL"])
            self._cache[text] = sentiment
            logger.info(f"Sentiment analyzed for text: '{text[:20]}...' → {sentiment}")

        time.sleep(len(text) * 0.01)

        return AnalyzeResponse(sentiment=sentiment)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sentiment_pb2_grpc.add_SentimentServicer_to_server(SentimentServicer(), server)
    server.add_insecure_port("[::]:50051")
    logger.info("gRPC Sentiment server listening on :50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
