import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from facenet_pytorch.models.mtcnn import MTCNN


@st.cache
def load_model(device=None):
    model = MTCNN(margin=0, device=device)
    return model


class VideoTransformer(VideoTransformerBase):
    def __init__(self) -> None:
        super().__init__()
        self.model = load_model()

    def transform(self, frame):
        image = frame.to_ndarray(format="bgr24")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes, probs, points = self.model.detect(image, landmarks=True)

        image_draw = image.copy()
        for box, box_points in zip(boxes, points):
            color = (0, 255, 0)

            box = box.astype(int)
            box = box.tolist()
            cv2.rectangle(image_draw, (box[0], box[1]), (box[2], box[3]), color, 2)
        
            for point in box_points:
                point = point.astype(int)
                point = point.tolist()
                cv2.rectangle(
                    image_draw, 
                    (point[0] - 1, point[1] - 1), 
                    (point[0] + 1, point[1] + 1), 
                    color, 
                    2,
                )

        image_draw = cv2.cvtColor(image_draw, cv2.COLOR_RGB2BGR)

        return image_draw


if __name__ == "__main__":
    st.title("MTCNN Stream Demo")
    webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)