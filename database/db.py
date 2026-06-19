import sqlite3
from datetime import date

DB_PATH = "financas.db"


def _connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transacoes (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id   INTEGER NOT NULL,
                tipo      TEXT    NOT NULL,
                valor     REAL    NOT NULL,
                descricao TEXT    NOT NULL,
                data      TEXT    NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS recorrentes (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id   INTEGER NOT NULL,
                tipo      TEXT    NOT NULL,
                valor     REAL    NOT NULL,
                descricao TEXT    NOT NULL,
                desde     TEXT    NOT NULL
            )
        """)


def inserir_transacao(user_id: int, tipo: str, valor: float, descricao: str):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO transacoes (user_id, tipo, valor, descricao, data) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, tipo, valor, descricao, date.today().isoformat()),
        )


def totais_do_mes(user_id: int, ano_mes: str):
    """Retorna (total_ganhos, total_gastos) do mês informado (formato YYYY-MM)."""
    with _connect() as conn:
        linhas = conn.execute(
            "SELECT tipo, COALESCE(SUM(valor), 0) "
            "FROM transacoes "
            "WHERE user_id = ? AND strftime('%Y-%m', data) = ? "
            "GROUP BY tipo",
            (user_id, ano_mes),
        ).fetchall()

    totais = {"ganho": 0.0, "gasto": 0.0}
    for tipo, total in linhas:
        totais[tipo] = total
    return totais["ganho"], totais["gasto"]


def gastos_por_descricao(user_id: int, ano_mes: str):
    """Retorna lista de (descricao, total) dos gastos do mês, do maior para o menor."""
    with _connect() as conn:
        return conn.execute(
            "SELECT descricao, SUM(valor) AS total "
            "FROM transacoes "
            "WHERE user_id = ? AND tipo = 'gasto' AND strftime('%Y-%m', data) = ? "
            "GROUP BY descricao "
            "ORDER BY total DESC",
            (user_id, ano_mes),
        ).fetchall()


def inserir_recorrente(user_id: int, tipo: str, valor: float, descricao: str, desde: str):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO recorrentes (user_id, tipo, valor, descricao, desde) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, tipo, valor, descricao, desde),
        )


def listar_recorrentes(user_id: int):
    """Retorna todos os recorrentes do usuário: (id, tipo, valor, descricao, desde)."""
    with _connect() as conn:
        return conn.execute(
            "SELECT id, tipo, valor, descricao, desde "
            "FROM recorrentes "
            "WHERE user_id = ? "
            "ORDER BY id",
            (user_id,),
        ).fetchall()


def remover_recorrente(user_id: int, rec_id: int) -> int:
    """Remove um recorrente por id (restrito ao usuário). Retorna nº de linhas removidas."""
    with _connect() as conn:
        cursor = conn.execute(
            "DELETE FROM recorrentes WHERE id = ? AND user_id = ?",
            (rec_id, user_id),
        )
        return cursor.rowcount


def recorrentes_ativos_do_mes(user_id: int, ano_mes: str):
    """Retorna (tipo, valor, descricao) dos recorrentes ativos no mês (desde <= ano_mes)."""
    with _connect() as conn:
        return conn.execute(
            "SELECT tipo, valor, descricao "
            "FROM recorrentes "
            "WHERE user_id = ? AND desde <= ? "
            "ORDER BY id",
            (user_id, ano_mes),
        ).fetchall()
