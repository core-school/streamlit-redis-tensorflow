import asyncio
from redis.client import connect, disconnect, get_connection
from redis.serializer import parse
from config import REDIS_FRAMES_CHANNEL, REDIS_PREDICTIONS_CHANNEL
from predict.predict import inference


async def consume():
    await connect()
    other = await connect("other_connection")

    # Subscribe to our channel
    subscriber = await get_connection().start_subscribe()
    await subscriber.subscribe([REDIS_FRAMES_CHANNEL])

    # Inside a while loop, wait for incoming events.
    while True:
        msg = await subscriber.next_published()
        # receive frame
        frame = parse(msg.value)
        print(
            f"[channel: {msg.channel}] Received frame of size:", frame.shape)
        result = inference(frame)
        await other.publish(REDIS_PREDICTIONS_CHANNEL, result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(consume())
    except KeyboardInterrupt:
        # When finished, close the connection.
        loop.run_until_complete(disconnect())
