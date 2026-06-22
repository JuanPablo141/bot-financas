from datetime import date, datetime
from telegram import Update
from telegram.ext import ContextTypes
from database.db import inserir_transacao


def resolver_ano_mes(args):
    """Resolve o mês a partir dos argumentos do comando.

    Sem argumento → mês atual. Com argumento → valida o formato AAAA-MM.
    Retorna (ano_mes, valido): se o formato for inválido, retorna (None, False).
    """
    if not args:
        return date.today().strftime("%Y-%m"), True

    ano_mes = args[0]
    try:
        datetime.strptime(ano_mes, "%Y-%m")
    except ValueError:
        return None, False
    return ano_mes, True


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
