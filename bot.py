from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Данные храним в памяти
chats_data = {}  # { chat_id: { "budget": float, "spent_total": float, "users": { user_id: {"name": str, "spent": float} } } }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для контроля бюджета.\n\n"
        "Команды:\n"
        "/set_budget <сумма> — задать бюджет\n"
        "/status — показать текущий статус\n"
        "/top — рейтинг по тратам\n"
        "/reset_budget — сбросить бюджет\n"
        "Чтобы добавить трату, просто отправь число."
    )

async def set_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Укажи сумму: /set_budget 10000")
        return

    try:
        amount = float(context.args[0])
    except ValueError:
        await update.message.reply_text("Нужно указать число, например: /set_budget 10000")
        return

    chat_id = update.message.chat_id
    chats_data[chat_id] = {"budget": amount, "spent_total": 0, "users": {}}

    await update.message.reply_text(f"✅ Бюджет установлен: {amount}")

async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text)
    except ValueError:
        return  # Игнорируем текст, который не является числом

    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    user_name = update.message.from_user.full_name

    if chat_id not in chats_data:
        await update.message.reply_text("Сначала установи бюджет командой /set_budget")
        return

    # Обновляем траты
    chats_data[chat_id]["spent_total"] += amount
    if user_id not in chats_data[chat_id]["users"]:
        chats_data[chat_id]["users"][user_id] = {"name": user_name, "spent": 0}
    chats_data[chat_id]["users"][user_id]["spent"] += amount

    remaining = chats_data[chat_id]["budget"] - chats_data[chat_id]["spent_total"]

    await update.message.reply_text(
        f"✅ {user_name} добавил трату {amount}\n"
        f"Остаток бюджета: {remaining}"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id not in chats_data:
        await update.message.reply_text("Бюджет не установлен.")
        return

    data = chats_data[chat_id]
    text = (
        f"📊 Бюджет: {data['budget']}\n"
        f"💸 Потрачено: {data['spent_total']}\n"
        f"Остаток: {data['budget'] - data['spent_total']}\n\n"
        f"Траты по участникам:\n"
    )

    for user in data["users"].values():
        text += f"- {user['name']}: {user['spent']}\n"

    await update.message.reply_text(text)

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id not in chats_data or not chats_data[chat_id]["users"]:
        await update.message.reply_text("Нет данных по тратам.")
        return

    sorted_users = sorted(chats_data[chat_id]["users"].values(), key=lambda x: x["spent"], reverse=True)
    text = "🏆 ТОП участников по тратам:\n"
    for idx, user in enumerate(sorted_users, start=1):
        text += f"{idx}. {user['name']} — {user['spent']}\n"

    await update.message.reply_text(text)

async def reset_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    chats_data[chat_id] = {"budget": 0, "spent_total": 0, "users": {}}
    await update.message.reply_text("✅ Бюджет сброшен!")

app = ApplicationBuilder().token("8220413192:AAGupQhhdCxuZmrEwTHkOHjg2v9QcEkxDrU").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("set_budget", set_budget))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("top", top))
app.add_handler(CommandHandler("reset_budget", reset_budget))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_expense))

print("✅ Бот запущен! Ждёт команды...")  # <-- добавили
app.run_polling()