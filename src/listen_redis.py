import asyncio
from redis.client import connect, get_connection
from config import REDIS_PREDICTIONS_CHANNEL
from streamlit.script_run_context import add_script_run_ctx
from threading import Thread

global prediction
prediction = "nothing"


def get_current_prediction():
    return prediction


async def prepare_redis():
    await connect()
    await connect("frames_connection")

    # Subscribe to predictions
    subscriber = await get_connection().start_subscribe()
    await subscriber.subscribe([REDIS_PREDICTIONS_CHANNEL])
    print("💪🏻 Waiting for predictions...")

    # Inside a while loop, wait for incoming events.
    global prediction
    while True:
        msg = await subscriber.next_published()
        prediction = msg.value
        print(f"[channel: {msg.channel}] Prediction: {prediction}")


def start_prediction_thread():
    predictions_loop = asyncio.new_event_loop()

    def run_forever():
        print("✅ Prediction thread is started")
        asyncio.set_event_loop(predictions_loop)
        predictions_loop.run_until_complete(prepare_redis())
    # Run coros in bg thread
    thread = Thread(target=run_forever, daemon=True)
    add_script_run_ctx(thread)
    thread.start()
