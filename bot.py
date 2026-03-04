from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import random

# Твой Telegram токен
BOT_TOKEN = "ВАШ_TELEGRAM_BOT_TOKEN"

# Список дерзких фраз для флирта
flirt_phrases = [
    "О, ты снова здесь… 😏",
    "Я думала о тебе весь день… 💋",
    "Не пытайся убежать от моего взгляда 😉",
    "Ты слишком милый, чтобы просто так проходить мимо 😈",
    "Хочешь, я расскажу тебе секрет? Только тебе… 🔥",
    "Твои сообщения заставляют меня улыбаться 😇",
]

# Приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет 😘 Я твоя игривая помощница. Напиши что-нибудь — и я отвечу дерзко!"
    )

# Основной обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:
        response = random.choice(flirt_phrases)
        await update.message.reply_text(response)

# Основная функция запуска
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен…")
    app.run_polling()

if __name__ == "__main__":
    main()
