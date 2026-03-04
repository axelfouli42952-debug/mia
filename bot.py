import os
import base64
from io import BytesIO
from random import choice
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from huggingface_hub import InferenceClient
from PIL import Image

# === 1. Настройки ===
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

hf_client = InferenceClient(token=HF_TOKEN)
MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"

# Фразы для флирта
FLIRTY_PHRASES = [
    "Смотри, это я 😏",
    "Только для тебя, не показывай никому 😉",
    "А тебе нравится, когда я улыбаюсь? 😘",
    "Я могла бы позировать целый день для тебя 😎",
    "Готовься к небольшому флирту вместе с фото 😇"
]

# === 2. Генерация изображения ===
def generate_image(prompt: str) -> BytesIO:
    response = hf_client.text_to_image(prompt=prompt, model=MODEL_ID)
    img_data = base64.b64decode(response["image_base64"])
    image_bytes = BytesIO(img_data)
    image_bytes.seek(0)
    return image_bytes

# === 3. Обработчик команды /photo ===
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    prompt = "A photorealistic portrait of a beautiful young woman, smiling, playful expression, realistic lighting"

    await update.message.reply_text(f"{user}, подожди немного, генерирую фото... 📸")
    
    try:
        image_bytes = generate_image(prompt)
        # Сначала отправляем фото
        await update.message.reply_photo(photo=image_bytes)
        # Затем отправляем дерзкую фразу
        flirty_message = choice(FLIRTY_PHRASES)
        await update.message.reply_text(flirty_message)
    except Exception as e:
        await update.message.reply_text(f"Ошибка при генерации фото: {e}")

# === 4. Запуск бота ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("photo", photo_handler))
    print("Бот с флиртом запущен...")
    app.run_polling()
