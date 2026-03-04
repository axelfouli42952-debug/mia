# bot.py
import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from httpx import AsyncClient

# =========================
# 1. Настройки
# =========================
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Твой токен Telegram
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")  # Твой ключ Mistral
MISTRAL_MODEL = "mistralai/mistral-instruct-7B-v0.1"  # Пример модели

# =========================
# 2. Функция генерации текста с Mistral
# =========================
async def generate_flirt(prompt: str) -> str:
    url = f"https://api.mistral.ai/v1/models/{MISTRAL_MODEL}/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "input": prompt,
        "max_tokens": 200,
        "temperature": 0.8
    }

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        # Mistral возвращает текст здесь
        return result["completions"][0]["text"]

# =========================
# 3. Обработчики Telegram
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я могу немного флиртовать 😉 Напиши что-нибудь!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    # Формируем подсказку для бота
    prompt = f"Флирт с пользователем: {user_text}\nОтвети игриво, но безопасно."
    try:
        reply = await generate_flirt(prompt)
    except Exception as e:
        reply = "Упс, что-то пошло не так 😅"
        print("Ошибка генерации:", e)

    await update.message.reply_text(reply)

# =========================
# 4. Основная функция
# =========================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота через polling (можно на Railway)
    app.run_polling()

if __name__ == "__main__":
    main()
