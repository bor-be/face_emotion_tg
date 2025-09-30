import requests
import os
from io import BytesIO
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from face_detector import detect_and_crop_face_bytes
from dotenv import load_dotenv

load_dotenv()  

TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Пришли мне фото, и я распознаю эмоцию.")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Пожалуйста, пришли картинку с лицом.")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_bytes = await file.download_as_bytearray()

    face_bytes = detect_and_crop_face_bytes(file_bytes)
    if not face_bytes:
        await update.message.reply_text("Лицо не найдено, попробуй другое фото.")
        return

    # Отправляем обрезанное лицо пользователю
    # await update.message.reply_photo(photo=face_bytes, caption="Вот обрезанное лицо!")

    try:
        with BytesIO(face_bytes) as f:
            response = requests.post(API_URL, files={"file": f}).json()
        emotion = response.get("emotion", "Не удалось распознать")
        confidence = response.get("confidence", 0)
        await update.message.reply_text(
            f"Эмоция: {emotion}\nУверенность: {confidence:.2f}"
        )
    except Exception as e:
        await update.message.reply_text(f"Ошибка при распознавании эмоции: {e}")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
