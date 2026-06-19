from datetime import date, datetime
from telegram import Update
from telegram.ext import ContextTypes
from database.db import (
    totais_do_mes,
    gastos_por_descricao,
    recorrentes_ativos_do_mes,
)


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

    # Recorrentes ativos no mês são somados virtualmente aos totais.
    recorrentes = recorrentes_ativos_do_mes(user_id, ano_mes)
    gastos_recorrentes = {}
    for tipo, valor, descricao in recorrentes:
        if tipo == "ganho":
            total_ganhos += valor
        else:
            total_gastos += valor
            gastos_recorrentes[descricao] = gastos_recorrentes.get(descricao, 0.0) + valor

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

    # Mescla os gastos avulsos com os recorrentes, somando por descrição.
    gastos = dict(gastos_por_descricao(user_id, ano_mes))
    for descricao, valor in gastos_recorrentes.items():
        gastos[descricao] = gastos.get(descricao, 0.0) + valor

    if gastos:
        linhas.append("")
        linhas.append("Gastos por descrição:")
        for descricao, total in sorted(gastos.items(), key=lambda x: x[1], reverse=True):
            linhas.append(f"• {descricao} — R$ {total:.2f}")

    if recorrentes:
        n = len(recorrentes)
        plural = "lançamento recorrente" if n == 1 else "lançamentos recorrentes"
        linhas.append("")
        linhas.append(f"(inclui {n} {plural})")

    await update.message.reply_text("\n".join(linhas))
