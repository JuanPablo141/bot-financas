from telegram import Update
from telegram.ext import ContextTypes
from handlers._helpers import registrar_transacao


async def gasto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await registrar_transacao(update, context, "gasto", "Gasto")
