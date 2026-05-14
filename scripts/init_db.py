from __future__ import annotations

import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "miraflor.sqlite3"
SCHEMA_PATH = ROOT / "data" / "schema.sql"

PLAYERS = [
    (1, "Juan Perez", "Portero", 1, 24, "1.85m", "/img/portero.png", "Especialista en penaltis y gran reflejo bajo palos."),
    (2, "Carlos Martin", "Defensa", 4, 23, "1.80m", "/img/portero.png", "Central contundente y seguro en el juego aereo."),
    (3, "David Lopez", "Centrocampista", 8, 25, "1.76m", "/img/portero.png", "Organiza el juego y marca el ritmo del equipo."),
    (4, "Miguel Sanchez", "Delantero", 9, 22, "1.82m", "/img/portero.png", "Referencia ofensiva con buen remate dentro del area."),
    (5, "Alvaro Garcia", "Extremo", 11, 21, "1.74m", "/img/portero.png", "Jugador rapido, vertical y con desborde."),
]

MATCHES = [
    (1, "2025-09-14 11:00", "Municipal Arroyomolinos", "Cultural Deportiva Miraflor", 5, 0, "jugado"),
    (2, "2025-09-21 11:00", "Cultural Deportiva Miraflor", "CD Grinon B", 1, 0, "jugado"),
    (3, "2025-09-28 17:00", "Villa del Prado", "Cultural Deportiva Miraflor", 4, 3, "jugado"),
    (4, "2025-10-05 18:30", "Cultural Deportiva Miraflor", "Mostoles CF", 1, 1, "jugado"),
    (5, "2025-10-12 16:00", "EF At. Casarrubuelos", "Cultural Deportiva Miraflor", 3, 0, "jugado"),
    (6, "2025-10-19 17:00", "Cultural Deportiva Miraflor", "Union FC", 2, 1, "jugado"),
    (7, "2025-10-26 11:00", "Lucero-Linces", "Cultural Deportiva Miraflor", 3, 4, "jugado"),
    (8, "2025-11-02 17:00", "Cultural Deportiva Miraflor", "Humanes", 2, 1, "jugado"),
    (9, "2025-11-09 16:30", "Atletico Valdeiglesias", "Cultural Deportiva Miraflor", 3, 0, "jugado"),
    (10, "2025-11-16 17:00", "Cultural Deportiva Miraflor", "UD Mostoles Balompie", 2, 2, "jugado"),
    (11, "2025-11-23 12:15", "Amistad Alcorcon A", "Cultural Deportiva Miraflor", 2, 1, "jugado"),
    (12, "2025-11-30 17:00", "Cultural Deportiva Miraflor", "Fepe Getafe III", 3, 1, "jugado"),
    (13, "2025-12-14 12:00", "Nuevo Boadilla", "Cultural Deportiva Miraflor", 2, 2, "jugado"),
    (14, "2025-12-21 19:30", "Cultural Deportiva Miraflor", "Ciudad de Getafe SC", 0, 2, "jugado"),
    (15, "2026-01-11 17:00", "Cultural Deportiva Miraflor", "Leganes C", 2, 0, "jugado"),
    (16, "2026-01-18 11:15", "CD Los Yebenes-San Bruno", "Cultural Deportiva Miraflor", 4, 2, "jugado"),
    (17, "2026-01-25 17:00", "Cultural Deportiva Miraflor", "Moraleja de Enmedio", 2, 3, "jugado"),
    (18, "2026-02-01 17:00", "Cultural Deportiva Miraflor", "Municipal Arroyomolinos", 0, 6, "jugado"),
    (19, "2026-02-08 11:30", "CD Grinon B", "Cultural Deportiva Miraflor", 5, 3, "jugado"),
    (20, "2026-02-15 17:00", "Cultural Deportiva Miraflor", "Villa del Prado", 2, 3, "jugado"),
    (21, "2026-02-22 13:15", "Mostoles CF", "Cultural Deportiva Miraflor", 2, 0, "jugado"),
    (22, "2026-03-01 17:00", "Cultural Deportiva Miraflor", "EF At. Casarrubuelos", 3, 0, "jugado"),
    (23, "2026-03-08 15:00", "Union FC", "Cultural Deportiva Miraflor", 1, 1, "jugado"),
    (24, "2026-03-15 17:00", "Cultural Deportiva Miraflor", "Lucero-Linces", 1, 2, "jugado"),
    (25, "2026-03-22 12:00", "Humanes", "Cultural Deportiva Miraflor", 1, 0, "jugado"),
    (26, "2026-03-29 17:00", "Cultural Deportiva Miraflor", "Atletico Valdeiglesias", 3, 2, "jugado"),
    (27, "2026-04-12 17:30", "UD Mostoles Balompie", "Cultural Deportiva Miraflor", 5, 0, "jugado"),
    (28, "2026-04-19 17:00", "Cultural Deportiva Miraflor", "Amistad Alcorcon A", 2, 2, "jugado"),
    (29, "2026-04-26 16:00", "Fepe Getafe III", "Cultural Deportiva Miraflor", 2, 0, "jugado"),
    (30, "2026-05-10 17:00", "Cultural Deportiva Miraflor", "Nuevo Boadilla", 1, 2, "jugado"),
    (31, "2026-05-17 18:00", "Ciudad de Getafe SC", "Cultural Deportiva Miraflor", None, None, "por_jugar"),
    (32, "2026-05-24 00:00", "Leganes C", "Cultural Deportiva Miraflor", None, None, "por_jugar"),
    (33, "2026-05-31 00:00", "Cultural Deportiva Miraflor", "CD Los Yebenes-San Bruno", None, None, "por_jugar"),
    (34, "2026-06-07 00:00", "Moraleja de Enmedio", "Cultural Deportiva Miraflor", None, None, "por_jugar"),
]


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.executemany(
            """
            INSERT OR REPLACE INTO jugadores
            (id, nombre, posicion, dorsal, edad, altura, foto, descripcion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            PLAYERS,
        )
        conn.executemany(
            """
            INSERT OR REPLACE INTO partidos
            (jornada, fecha, local, visitante, goles_local, goles_visitante, estado)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            MATCHES,
        )
        conn.commit()

    print(f"Base de datos creada en {DB_PATH}")


if __name__ == "__main__":
    main()
