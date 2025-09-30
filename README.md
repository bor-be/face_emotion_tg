# Face Emotion Recognition Bot

Проект для распознавания эмоций на лице с помощью ResNet34, FastAPI и Telegram-бота.

Клонируем репозиторий и переходим в папку проекта, создаём `.env` и запускаем Docker Compose:

```bash
git clone https://github.com/bor-be/face_emotion_tg.git
cd face_emotion_tg

# создаём .env
echo "BOT_TOKEN=<токен вашего Telegram бота>" >> .env
echo "API_URL=http://face-emotion-app:8000/predict" >> .env

# запуск
docker-compose up --build
