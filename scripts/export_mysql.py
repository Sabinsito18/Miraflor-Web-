from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SQLITE_DB = ROOT / "data" / "miraflor.sqlite3"
MYSQL_SQL = ROOT / "data" / "miraflor_mysql.sql"


def sql_value(value: Any) -> str:
    if value is None:
        return "NULL"

    if isinstance(value, int):
        return str(value)

    text = str(value).replace("\\", "\\\\").replace("'", "''")
    return f"'{text}'"


def insert_statement(table: str, columns: list[str], row: sqlite3.Row) -> str:
    column_sql = ", ".join(f"`{column}`" for column in columns)
    value_sql = ", ".join(sql_value(row[column]) for column in columns)
    return f"INSERT INTO `{table}` ({column_sql}) VALUES ({value_sql});"


def main() -> None:
    if not SQLITE_DB.exists():
        raise SystemExit("No existe data/miraflor.sqlite3. Ejecuta primero: py scripts/init_db.py")

    conn = sqlite3.connect(SQLITE_DB)
    conn.row_factory = sqlite3.Row

    jugadores = conn.execute("SELECT * FROM jugadores ORDER BY id").fetchall()
    partidos = conn.execute("SELECT * FROM partidos ORDER BY jornada").fetchall()
    inscripciones = conn.execute("SELECT * FROM inscripciones ORDER BY id").fetchall()

    lines = [
        "-- Base de datos A.C.D. Miraflor para MySQL",
        "-- Generado desde data/miraflor.sqlite3",
        "CREATE DATABASE IF NOT EXISTS `miraflor` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
        "USE `miraflor`;",
        "",
        "SET FOREIGN_KEY_CHECKS = 0;",
        "DROP TABLE IF EXISTS `inscripciones`;",
        "DROP TABLE IF EXISTS `partidos`;",
        "DROP TABLE IF EXISTS `jugadores`;",
        "SET FOREIGN_KEY_CHECKS = 1;",
        "",
        "CREATE TABLE `jugadores` (",
        "  `id` INT NOT NULL,",
        "  `nombre` VARCHAR(120) NOT NULL,",
        "  `posicion` VARCHAR(60) NOT NULL,",
        "  `dorsal` INT NOT NULL,",
        "  `edad` INT NULL,",
        "  `altura` VARCHAR(20) NULL,",
        "  `foto` VARCHAR(255) NULL,",
        "  `descripcion` TEXT NULL,",
        "  PRIMARY KEY (`id`),",
        "  UNIQUE KEY `uq_jugadores_dorsal` (`dorsal`)",
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;",
        "",
        "CREATE TABLE `partidos` (",
        "  `id` INT NOT NULL,",
        "  `jornada` INT NOT NULL,",
        "  `fecha` DATETIME NOT NULL,",
        "  `local` VARCHAR(160) NOT NULL,",
        "  `visitante` VARCHAR(160) NOT NULL,",
        "  `goles_local` INT NULL,",
        "  `goles_visitante` INT NULL,",
        "  `estado` ENUM('jugado', 'por_jugar') NOT NULL,",
        "  `competicion` VARCHAR(160) NOT NULL DEFAULT 'Preferente Madrid Grupo 4',",
        "  `temporada` VARCHAR(20) NOT NULL DEFAULT '2025/2026',",
        "  PRIMARY KEY (`id`),",
        "  UNIQUE KEY `uq_partidos_jornada` (`jornada`)",
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;",
        "",
        "CREATE TABLE `inscripciones` (",
        "  `id` INT NOT NULL AUTO_INCREMENT,",
        "  `nombre_alumno` VARCHAR(120) NOT NULL,",
        "  `apellidos_alumno` VARCHAR(160) NOT NULL,",
        "  `fecha_nacimiento` DATE NOT NULL,",
        "  `categoria` VARCHAR(60) NOT NULL,",
        "  `experiencia` VARCHAR(120) NULL,",
        "  `tutor` VARCHAR(180) NOT NULL,",
        "  `telefono` VARCHAR(40) NOT NULL,",
        "  `email` VARCHAR(180) NOT NULL,",
        "  `observaciones` TEXT NULL,",
        "  `privacidad` TINYINT(1) NOT NULL DEFAULT 1,",
        "  `creada_en` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,",
        "  PRIMARY KEY (`id`)",
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;",
        "",
    ]

    for row in jugadores:
        lines.append(insert_statement("jugadores", list(row.keys()), row))

    lines.append("")

    for row in partidos:
        lines.append(insert_statement("partidos", list(row.keys()), row))

    if inscripciones:
        lines.append("")
        for row in inscripciones:
            lines.append(insert_statement("inscripciones", list(row.keys()), row))

    lines.append("")
    lines.append("-- Fin del volcado MySQL")

    MYSQL_SQL.write_text("\n".join(lines), encoding="utf-8")
    print(f"Archivo MySQL creado en {MYSQL_SQL}")


if __name__ == "__main__":
    main()
