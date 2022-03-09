from redis.client import connect, disconnect, get_connection
from config import REDIS_FRAMES_CHANNEL
import asyncio
import numpy as np
import pickle
import codecs
from redis.serializer import serialize

default_color_frame = np.zeros((100, 100, 3))


async def send_frame(frame=default_color_frame, connection_id="default"):
    raw_frame = serialize(frame)
    await get_connection(connection_id).publish(REDIS_FRAMES_CHANNEL, raw_frame)
    print("🚀 Sent frame to redis")


async def test_produce():
    # Create Redis connection
    await connect()
    send_frame()
    await disconnect()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_produce())
