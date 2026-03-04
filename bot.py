import os
import requests

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Токены
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = os.getenv("HF_TOKEN")

MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"

# Функция запроса к Hugging Face Chat Completion API
def get_mistral_reply(user_message: str) -> str:
    url = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json",
    }
    
    # Формируем сообщения для чат‑инференса
    payload = {
        "inputs": {
            "messages": [
                {"role": "system", "content": "Ты Мия — игривая, дерзкая, флиртующая девушка."},
                {"role": "user", "content": user_message}
            ]
        },
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.9,
            "top_p": 0.9
        }
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        return "Похоже, я не могу ответить сейчас 😅"
    
    data = response.json()
    # Получаем ответ из структуры HF
    try:
        # В инференсе Mistral ответ лежит тут
        return data["generated_text"]
    except:
        return "Что‑то пошло не так 😬"

# Обработчик Telegram сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # Запрос к модели
    reply = get_mistral_reply(text)
    
    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен…")
    app.run_polling()

