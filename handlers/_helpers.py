from telegram import Update
from telegram.ext import ContextTypes
from database.db import inserir_transacao


async def registrar_transacao(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    tipo: str,
    label: str,
):
    comando = "gasto" if tipo == "gasto" else "ganho"

    if len(context.args) < 2:
        await update.message.reply_text(
            f"Uso correto: /{comando} <valor> <descrição>\n"
            f"Exemplo: /{comando} 50 almoço"
        )
        return

    try:
        valor = float(context.args[0].replace(",", "."))
    except ValueError:
        await update.message.reply_text(
            "Valor inválido. Use um número.\n"
            f"Exemplo: /{comando} 50 almoço"
        )
        return

    descricao = " ".join(context.args[1:])
    user_id = update.effective_user.id

    inserir_transacao(user_id, tipo, valor, descricao)

    await update.message.reply_text(
        f"{label} de R$ {valor:.2f} ({descricao}) registrado!"
    )
