from __future__ import annotations

import json
import mimetypes
import os
import sqlite3
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "miraflor.sqlite3"
SCHEMA_PATH = ROOT / "data" / "schema.sql"


def row_to_dict(row: sqlite3.Row) -> dict:
    return {key: row[key] for key in row.keys()}


def get_connection() -> sqlite3.Connection:
    ensure_database()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_database() -> None:
    if DB_PATH.exists():
        return

    from scripts.init_db import main as init_database

    init_database()


class MiraflorHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        path = urlparse(self.path).path

        if path == "/api/jugadores":
            self.send_json(self.fetch_all("SELECT * FROM jugadores ORDER BY dorsal"))
            return

        if path == "/api/partidos":
            self.send_json(self.fetch_all("SELECT * FROM partidos ORDER BY jornada"))
            return

        if path == "/api/inscripciones":
            self.send_json(self.fetch_all("SELECT * FROM inscripciones ORDER BY creada_en DESC"))
            return

        super().do_GET()

    def do_POST(self) -> None:
        path = urlparse(self.path).path

        if path != "/api/inscripciones":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        payload = self.read_json()
        required = [
            "nombre_alumno",
            "apellidos_alumno",
            "fecha_nacimiento",
            "categoria",
            "tutor",
            "telefono",
            "email",
        ]

        missing = [field for field in required if not payload.get(field)]
        if missing:
            self.send_json({"error": "Faltan campos obligatorios", "missing": missing}, HTTPStatus.BAD_REQUEST)
            return

        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO inscripciones
                (nombre_alumno, apellidos_alumno, fecha_nacimiento, categoria, experiencia,
                 tutor, telefono, email, observaciones, privacidad)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["nombre_alumno"],
                    payload["apellidos_alumno"],
                    payload["fecha_nacimiento"],
                    payload["categoria"],
                    payload.get("experiencia", ""),
                    payload["tutor"],
                    payload["telefono"],
                    payload["email"],
                    payload.get("observaciones", ""),
                    1 if payload.get("privacidad", True) else 0,
                ),
            )
            conn.commit()

        self.send_json({"ok": True, "id": cursor.lastrowid}, HTTPStatus.CREATED)

    def fetch_all(self, query: str) -> list[dict]:
        with get_connection() as conn:
            return [row_to_dict(row) for row in conn.execute(query).fetchall()]

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw or "{}")

    def send_json(self, data: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    ensure_database()

    mimetypes.add_type("text/css", ".css")
    mimetypes.add_type("application/javascript", ".js")

    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))

    server = ThreadingHTTPServer((host, port), MiraflorHandler)
    print(f"Web Miraflor lista en http://{host}:{port}")
    print("API: /api/jugadores, /api/partidos, /api/inscripciones")
    server.serve_forever()


if __name__ == "__main__":
    main()
