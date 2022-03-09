from streamlit_webrtc import VideoProcessorBase, webrtc_streamer, WebRtcMode
from av import VideoFrame
import asyncio
from redis.produce import send_frame
import cv2
from listen_redis import get_current_prediction, start_prediction_thread


def send_frame_task(frame_data):
    # # @boyander: send task to bg thread and forget
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
            # Convert frame to numpy array and send it to bg thread to redis
            frame_data = frame.to_ndarray()
            send_frame_task(frame_data)
            self.frame_count = 0
        else:
            self.frame_count += 1

        # Add prediction to frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        frame = cv2.putText(frame.to_ndarray(format="bgr24"), f"Prediction: {get_current_prediction()}", org, font,
                            fontScale, color, thickness, cv2.LINE_AA)

        return VideoFrame.from_ndarray(frame, format="bgr24")


webrtc_ctx = webrtc_streamer(
    key="Sign_Interpreter",
    mode=WebRtcMode.SENDRECV,
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)

start_prediction_thread()
