from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from sqlite3 import Connection, Cursor
from typing import Optional

DB_PATH = Path("..").joinpath("app.db")


@dataclass
class ConnectionProvider:
    _connection: Optional[Connection] = field(default=None, init=False)

    @classmethod
    def get_connection(cls) -> Connection:
        if cls._connection is None:
            cls._connection = sqlite3.connect(DB_PATH, check_same_thread=False)

        return cls._connection


def create_tables(cursor: Cursor, connection: Connection) -> None:
    cursor.execute("DROP TABLE IF EXISTS users;")
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT);")
    connection.commit()


def main() -> None:
    connection = ConnectionProvider.get_connection()
    cursor = connection.cursor()
    create_tables(cursor, connection)
    connection.close()


if __name__ == "__main__":
    main()
