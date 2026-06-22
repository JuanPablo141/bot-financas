from telegram import Update
from telegram.ext import ContextTypes
from database.db import gastos_consolidados_do_mes
from handlers._helpers import resolver_ano_mes
from utils.charts import pizza_gastos


async def grafico_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ano_mes, valido = resolver_ano_mes(context.args)
    if not valido:
        await update.message.reply_text(
            "Formato de mês inválido. Use AAAA-MM.\n"
            "Exemplo: /grafico 2026-05"
        )
        return

    user_id = update.effective_user.id
    dados = gastos_consolidados_do_mes(user_id, ano_mes)

    if not dados:
        await update.message.reply_text(f"Nenhum gasto registrado em {ano_mes}.")
        return

    imagem = pizza_gastos(dados, f"Gastos de {ano_mes}")
    await update.message.reply_photo(photo=imagem, caption=f"Gastos de {ano_mes}")
