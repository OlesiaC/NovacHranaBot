from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает!")

app = ApplicationBuilder().token("8220413192:AAGupQhhdCxuZmrEwTHkOHjg2v9QcEkxDrU").build()

app.add_handler(CommandHandler("start", start))

print("✅ Тестовый бот запущен. Напиши /start боту в Telegram.")
app.run_polling()