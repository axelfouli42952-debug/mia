import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import io

# Логи
logging.basicConfig(level=logging.INFO)

import os
BOT_TOKEN = os.environ.get("BOT_TOKEN")
HF_TOKEN = "YOUR_HF_TOKEN"

HF_MODEL = "stabilityai/stable-diffusion-2-1"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я могу сгенерировать фото девушки и флиртовать 😏\nНапиши что-нибудь, чтобы начать!"
    )

# Генерация фото через HF
def generate_image(prompt: str):
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    data = {"inputs": prompt}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return io.BytesIO(response.content)

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    
    prompt = "realistic photo of a young woman, smiling, studio lighting, 4k"
    try:
        image_bytes = generate_image(prompt)
        await update.message.reply_photo(photo=image_bytes, caption="Вот твоя девушка 😈")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при генерации фото: {e}")
        return

    flirt_text = "Привет 😏 Ты мне очень нравишься! Что делаем дальше?"
    await update.message.reply_text(flirt_text)

# Запуск бота
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    print("Бот запущен!")
    app.run_polling()

