from datetime import date, datetime
from telegram import Update
from telegram.ext import ContextTypes
from database.db import totais_do_mes, gastos_por_descricao


async def resumo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        ano_mes = context.args[0]
        try:
            datetime.strptime(ano_mes, "%Y-%m")
        except ValueError:
            await update.message.reply_text(
                "Formato de mês inválido. Use AAAA-MM.\n"
                "Exemplo: /resumo 2026-05"
            )
            return
    else:
        ano_mes = date.today().strftime("%Y-%m")

    user_id = update.effective_user.id
    total_ganhos, total_gastos = totais_do_mes(user_id, ano_mes)

    if total_ganhos == 0 and total_gastos == 0:
        await update.message.reply_text(
            f"Nenhuma transação registrada em {ano_mes}."
        )
        return

    saldo = total_ganhos - total_gastos

    linhas = [
        f"📊 Resumo de {ano_mes}",
        "",
        f"Ganhos:  R$ {total_ganhos:.2f}",
        f"Gastos:  R$ {total_gastos:.2f}",
        f"Saldo:   R$ {saldo:.2f}",
    ]

    gastos = gastos_por_descricao(user_id, ano_mes)
    if gastos:
        linhas.append("")
        linhas.append("Gastos por descrição:")
        for descricao, total in gastos:
            linhas.append(f"• {descricao} — R$ {total:.2f}")

    await update.message.reply_text("\n".join(linhas))
