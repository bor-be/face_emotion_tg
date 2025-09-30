# Face Emotion Recognition Bot

Проект для распознавания эмоций на лице с помощью ResNet34, FastAPI и Telegram-бота.

---

## Установка и запуск

### 1. Клонируем репозиторий

```bash
git clone https://github.com/bor-be/face_emotion_tg.git
cd face_emotion_tg

### Создай файл .env с переменными:
### BOT_TOKEN=<токен вашего Telegram бота>
### API_URL=http://face-emotion-app:8000/predict

### Запуск через Docker Compose
docker-compose up --build
