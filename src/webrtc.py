from config import REDIS_PREDICTIONS_CHANNEL
from streamlit_webrtc import VideoProcessorBase, webrtc_streamer, WebRtcMode
from av import VideoFrame
import asyncio
from redis.client import connect, get_connection
from redis.produce import send_frame
from threading import Thread
from streamlit.script_run_context import add_script_run_ctx


async def prepare_redis():
    await connect()
    await connect("frames_connection")

    # Subscribe to predictions
    subscriber = await get_connection().start_subscribe()
    await subscriber.subscribe([REDIS_PREDICTIONS_CHANNEL])
    print("💪🏻 Waiting for predictions...")

    # Inside a while loop, wait for incoming events.
    while True:
        msg = await subscriber.next_published()
        prediction = msg.value
        print(f"[channel: {prediction}] Prediction:", msg)


def send_frame_task(frame):
    frame_data = frame.to_ndarray()
    # # @boyander: send task to bg thread and forget
    # task = loop.create_task(send_frame(frame_data))
    loop = asyncio.get_event_loop()
    loop.create_task(send_frame(frame_data, "frames_connection"))


class VideoProcessor(VideoProcessorBase):
    def __init__(self):
        self.sequence = []
        self.frame_count = 0
        self.label = "ready?"
        self.pronostico = ""
        self.predict_threshold = 100

    def recv(self, frame: VideoFrame) -> VideoFrame:

        if self.frame_count > self.predict_threshold:
            send_frame_task(frame)
            self.frame_count = 0
        else:
            self.frame_count += 1

        return frame


webrtc_ctx = webrtc_streamer(
    key="Sign_Interpreter",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)

predictions_loop = asyncio.new_event_loop()


def run_forever():
    print("Started BG Thread")
    asyncio.set_event_loop(predictions_loop)
    predictions_loop.run_until_complete(prepare_redis())
    # predictions_loop.run_forever()


# Run coros in bg thread
thread = Thread(target=run_forever, daemon=True)
add_script_run_ctx(thread)
thread.start()
