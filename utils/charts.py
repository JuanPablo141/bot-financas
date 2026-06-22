from io import BytesIO

import matplotlib

# Backend headless: não tenta abrir janela (necessário para gerar imagem no servidor).
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402  (precisa vir depois de use())


def pizza_gastos(dados, titulo: str) -> BytesIO:
    """Gera um gráfico de pizza dos gastos e retorna um buffer PNG em memória.

    dados: lista de (descricao, total).
    """
    descricoes = [descricao for descricao, _ in dados]
    valores = [valor for _, valor in dados]

    fig, ax = plt.subplots()
    ax.pie(valores, labels=descricoes, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")  # mantém a pizza circular
    ax.set_title(titulo)

    buffer = BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)  # libera a figura da memória
    buffer.seek(0)
    return buffer
