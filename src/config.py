import os

REDIS_HOST = os.getenv("REDIS_HOST", 'localhost')
REDIS_PORT = os.getenv("REDIS_PORT", '6379')
REDIS_FRAMES_CHANNEL = os.getenv("REDIS_FRAMES_CHANNEL", 'frames')
REDIS_PREDICTIONS_CHANNEL = os.getenv(
    "REDIS_PREDICTIONS_CHANNEL", 'predictions')
