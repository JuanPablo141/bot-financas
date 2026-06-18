from telegram import Update
from telegram.ext import ContextTypes
from database.db import inserir_gasto


async def gasto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "Uso correto: /gasto <valor> <descrição>\n"
            "Exemplo: /gasto 50 almoço"
        )
        return

    try:
        valor = float(context.args[0].replace(",", "."))
    except ValueError:
        await update.message.reply_text(
            "Valor inválido. Use um número.\n"
            "Exemplo: /gasto 50 almoço"
        )
        return

    descricao = " ".join(context.args[1:])
    user_id = update.effective_user.id

    inserir_gasto(user_id, valor, descricao)

    await update.message.reply_text(
        f"Gasto de R$ {valor:.2f} ({descricao}) registrado!"
    )
