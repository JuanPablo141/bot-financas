from datetime import date
from telegram import Update
from telegram.ext import ContextTypes
from database.db import (
    inserir_recorrente,
    listar_recorrentes,
    remover_recorrente,
)

TIPOS_VALIDOS = ("gasto", "ganho")


async def recorrente_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text(
            "Uso correto: /recorrente <gasto|ganho> <valor> <descrição>\n"
            "Exemplo: /recorrente gasto 1200 aluguel"
        )
        return

    tipo = context.args[0].lower()
    if tipo not in TIPOS_VALIDOS:
        await update.message.reply_text(
            "Tipo inválido. Use 'gasto' ou 'ganho'.\n"
            "Exemplo: /recorrente gasto 1200 aluguel"
        )
        return

    try:
        valor = float(context.args[1].replace(",", "."))
    except ValueError:
        await update.message.reply_text(
            "Valor inválido. Use um número.\n"
            "Exemplo: /recorrente gasto 1200 aluguel"
        )
        return

    descricao = " ".join(context.args[2:])
    desde = date.today().strftime("%Y-%m")
    user_id = update.effective_user.id

    inserir_recorrente(user_id, tipo, valor, descricao, desde)

    rotulo = "Gasto" if tipo == "gasto" else "Ganho"
    await update.message.reply_text(
        f"{rotulo} recorrente de R$ {valor:.2f} ({descricao}) cadastrado!\n"
        f"Será contado nos resumos a partir de {desde}."
    )


async def recorrentes_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    recorrentes = listar_recorrentes(user_id)

    if not recorrentes:
        await update.message.reply_text(
            "Você ainda não tem lançamentos recorrentes.\n"
            "Cadastre com: /recorrente <gasto|ganho> <valor> <descrição>"
        )
        return

    linhas = ["📌 Seus lançamentos recorrentes:", ""]
    for rec_id, tipo, valor, descricao, desde in recorrentes:
        linhas.append(
            f"#{rec_id} — {tipo} R$ {valor:.2f} ({descricao}) desde {desde}"
        )
    linhas.append("")
    linhas.append("Para remover: /recorrente_remover <id>")

    await update.message.reply_text("\n".join(linhas))


async def recorrente_remover_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text(
            "Uso correto: /recorrente_remover <id>\n"
            "Veja os ids com /recorrentes"
        )
        return

    try:
        rec_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text(
            "Id inválido. Use o número mostrado em /recorrentes."
        )
        return

    user_id = update.effective_user.id
    removidos = remover_recorrente(user_id, rec_id)

    if removidos:
        await update.message.reply_text(f"Recorrente #{rec_id} removido.")
    else:
        await update.message.reply_text(
            f"Nenhum recorrente com id #{rec_id} foi encontrado."
        )
