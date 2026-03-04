import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from huggingface_hub import HfApi

# Токены из окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

# Инициализация Hugging Face API
hf_api = HfApi()
model_id = "stabilityai/stable-diffusion-2"  # можно менять на любой генератор фото

async def flirt_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Простейший флирт
    response_text = f"Ооо, {update.message.from_user.first_name}, ты только что сказал: '{user_text}' 😉"

    # Отправляем текст
    await update.message.reply_text(response_text)

    # Генерация фото через Hugging Face Inference API
    prompt = "realistic portrait of a young woman, smiling, cinematic lighting"
    output = hf_api.text_to_image(prompt=prompt, token=HF_TOKEN)  # вернёт bytes

    # Сохраняем временно и отправляем
    with open("girl.png", "wb") as f:
        f.write(output)

    await update.message.reply_photo(photo=open("girl.png", "rb"))

# Настройка приложения
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, flirt_photo))

# Запуск
print("Бот запущен...")
app.run_polling()
