from fastapi import FastAPI, File, UploadFile
from PIL import Image
from main import predict_image

app = FastAPI(title="Emotion Recognition API")


@app.get("/test")
def read_root():
    return {"message": "API работает!"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    image = Image.open(file.file).convert("L")
    pred_class, confidence = predict_image(image)

    emotions = {
        0: "злой",
        1: "отвращение",
        2: "страх",
        3: "счастливый",
        4: "нейтральный",
        5: "грустный",
        6: "удивление",
    }

    return {
        "class_index": pred_class,
        "confidence": confidence,
        "emotion": emotions.get(pred_class, "Unknown"),
    }
