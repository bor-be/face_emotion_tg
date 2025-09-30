from ultralytics import YOLO
from PIL import Image
from io import BytesIO

face_model = YOLO("yolov8n-face.pt")


def detect_and_crop_face_bytes(image_bytes: bytes) -> bytes | None:
    img = Image.open(BytesIO(image_bytes)).convert("RGB")

    results = face_model(img)[0]

    if len(results.boxes) == 0:
        return None

    box = results.boxes.xyxy[0].tolist()
    x1, y1, x2, y2 = map(int, box)

    cropped_face = img.crop((x1, y1, x2, y2))

    # Вариант Ч/Б
    cropped_face = cropped_face.convert("L")

    buf = BytesIO()
    cropped_face.save(buf, format="JPEG")
    buf.seek(0)
    return buf.getvalue()
