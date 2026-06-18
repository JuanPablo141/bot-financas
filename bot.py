import logging
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from database.db import init_db
from handlers.gastos import gasto_command
from handlers.ganhos import ganho_command


load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Eu sou seu bot de controle financeiro.\n"
        "Use /help para ver os comandos disponíveis."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comandos disponíveis:\n"
        "/start — inicia o bot\n"
        "/help — mostra esta mensagem\n"
        "/gasto <valor> <descrição> — registra um gasto\n"
        "/ganho <valor> <descrição> — registra um ganho"
    )

if __name__ == "__main__":
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    init_db()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("gasto", gasto_command))
    app.add_handler(CommandHandler("ganho", ganho_command))

    print("Bot rodando...")
    app.run_polling()