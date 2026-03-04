import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from huggingface_hub import InferenceClient

import io

# Настройка логов
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "YOUR_TELEGRAM_TOKEN"  # в Railway через Secrets
HF_TOKEN = "YOUR_HF_TOKEN"         # в Railway через Secrets

# Hugging Face клиент
hf_client = InferenceClient(token=HF_TOKEN)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я могу сгенерировать фото девушки и флиртовать 😏\nНапиши что-нибудь, чтобы начать!")

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    
    # Генерация фото через Stable Diffusion
    prompt = "realistic photo of a young woman, smiling, studio lighting, 4k"
    image_bytes = hf_client.text_to_image(prompt, model="stabilityai/stable-diffusion-2-1")
    
    # Отправляем фото
    await update.message.reply_photo(photo=io.BytesIO(image_bytes), caption="Вот твоя девушка 😈")
    
    # Флирт-текст
    flirt_text = "Привет 😏 Ты мне очень нравишься! Что делаем дальше?"
    await update.message.reply_text(flirt_text)

# Основной запуск
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    print("Бот запущен!")
    app.run_polling()
