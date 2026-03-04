import os
import base64
from io import BytesIO
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from huggingface_hub import InferenceClient
from PIL import Image

# === 1. Настройки ===
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")  # твой Telegram Bot Token
HF_TOKEN = os.environ.get("HF_TOKEN")  # твой Hugging Face Token

# Инициализация клиента Hugging Face
hf_client = InferenceClient(token=HF_TOKEN)
MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"

# === 2. Функция генерации изображения ===
def generate_image(prompt: str) -> BytesIO:
    """
    Генерирует изображение по текстовому промпту через Hugging Face.
    Возвращает BytesIO объект с PNG картинкой.
    """
    response = hf_client.text_to_image(prompt=prompt, model=MODEL_ID)
    
    # Модель возвращает base64 изображение
    img_data = base64.b64decode(response["image_base64"])
    image_bytes = BytesIO(img_data)
    image_bytes.seek(0)
    return image_bytes

# === 3. Обработчик команды /photo ===
async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    prompt = "A photorealistic portrait of a beautiful young woman, smiling, realistic lighting"  # базовый промпт

    await update.message.reply_text(f"{user}, подожди, генерирую фото... 📸")
    
    try:
        image_bytes = generate_image(prompt)
        await update.message.reply_photo(photo=image_bytes)
    except Exception as e:
        await update.message.reply_text(f"Ошибка при генерации фото: {e}")

# === 4. Запуск бота ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("photo", photo_handler))
    print("Бот запущен...")
    app.run_polling()
