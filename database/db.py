import sqlite3
from datetime import date

DB_PATH = "financas.db"


def _connect():
    return sqlite3.connect(DB_PATH)


def init_db():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS gastos (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id   INTEGER NOT NULL,
                valor     REAL    NOT NULL,
                descricao TEXT    NOT NULL,
                data      TEXT    NOT NULL
            )
        """)


def inserir_gasto(user_id: int, valor: float, descricao: str):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO gastos (user_id, valor, descricao, data) VALUES (?, ?, ?, ?)",
            (user_id, valor, descricao, date.today().isoformat()),
        )
