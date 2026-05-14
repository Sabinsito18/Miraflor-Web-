from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SQLITE_DB = ROOT / "data" / "miraflor.sqlite3"
sys.path.insert(0, str(ROOT))

import server


def sqlite_rows(table: str) -> list[sqlite3.Row]:
    conn = sqlite3.connect(SQLITE_DB)
    conn.row_factory = sqlite3.Row
    return conn.execute(f"SELECT * FROM {table} ORDER BY id").fetchall()


def ensure_mysql_tables() -> None:
    statements = [
        """
        CREATE TABLE IF NOT EXISTS jugadores (
          id INT NOT NULL,
          nombre VARCHAR(120) NOT NULL,
          posicion VARCHAR(60) NOT NULL,
          dorsal INT NOT NULL,
          edad INT NULL,
          altura VARCHAR(20) NULL,
          foto VARCHAR(255) NULL,
          descripcion TEXT NULL,
          PRIMARY KEY (id),
          UNIQUE KEY uq_jugadores_dorsal (dorsal)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        """
        CREATE TABLE IF NOT EXISTS partidos (
          id INT NOT NULL,
          jornada INT NOT NULL,
          fecha DATETIME NOT NULL,
          local VARCHAR(160) NOT NULL,
          visitante VARCHAR(160) NOT NULL,
          goles_local INT NULL,
          goles_visitante INT NULL,
          estado ENUM('jugado', 'por_jugar') NOT NULL,
          competicion VARCHAR(160) NOT NULL DEFAULT 'Preferente Madrid Grupo 4',
          temporada VARCHAR(20) NOT NULL DEFAULT '2025/2026',
          PRIMARY KEY (id),
          UNIQUE KEY uq_partidos_jornada (jornada)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
        """
        CREATE TABLE IF NOT EXISTS inscripciones (
          id INT NOT NULL AUTO_INCREMENT,
          nombre_alumno VARCHAR(120) NOT NULL,
          apellidos_alumno VARCHAR(160) NOT NULL,
          fecha_nacimiento DATE NOT NULL,
          categoria VARCHAR(60) NOT NULL,
          experiencia VARCHAR(120) NULL,
          tutor VARCHAR(180) NOT NULL,
          telefono VARCHAR(40) NOT NULL,
          email VARCHAR(180) NOT NULL,
          observaciones TEXT NULL,
          privacidad TINYINT(1) NOT NULL DEFAULT 1,
          creada_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """,
    ]

    with server.get_connection() as conn:
        with conn.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)
        conn.commit()


def upsert(table: str, rows: list[sqlite3.Row]) -> None:
    if not rows:
        return

    columns = rows[0].keys()
    column_sql = ", ".join(f"`{column}`" for column in columns)
    placeholders = ", ".join(["%s"] * len(columns))
    updates = ", ".join(f"`{column}` = VALUES(`{column}`)" for column in columns if column != "id")
    query = f"""
        INSERT INTO `{table}` ({column_sql})
        VALUES ({placeholders})
        ON DUPLICATE KEY UPDATE {updates}
    """

    values = [tuple(row[column] for column in columns) for row in rows]

    with server.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(query, values)
        conn.commit()


def main() -> None:
    if not server.using_mysql():
        raise SystemExit("DB_ENGINE no es mysql. Revisa tu archivo .env.")

    ensure_mysql_tables()
    upsert("jugadores", sqlite_rows("jugadores"))
    upsert("partidos", sqlite_rows("partidos"))
    print("MySQL sincronizado: jugadores y partidos listos. La tabla inscripciones se conserva.")


if __name__ == "__main__":
    main()
