import numpy as np
import cv2
import streamlit as st
from facenet_pytorch.models.mtcnn import MTCNN


def get_images():
    uploaded_files = st.file_uploader("Choose a photo", accept_multiple_files=True)
    images = []
    for uploaded_file in uploaded_files:
        _stream = uploaded_file.getvalue()
        data = np.fromstring(_stream, dtype=np.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        images.append(image)
    return images


@st.cache
def load_model(device=None):
    model = MTCNN(margin=0, device=device)
    return model


if __name__ == "__main__":
    st.title("MTCNN Demo")

    model = load_model()

    images = get_images()
    for image in images:
        boxes, probs, points = model.detect(image, landmarks=True)

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
        
        container = st.container()

        container.header(f"Your image")
        container.image(image_draw)