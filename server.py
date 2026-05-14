from __future__ import annotations

import json
import mimetypes
import os
import sqlite3
from datetime import date, datetime
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "miraflor.sqlite3"


def load_env_file() -> None:
    env_path = ROOT / ".env"

    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file()


def using_mysql() -> bool:
    return os.environ.get("DB_ENGINE", "sqlite").lower() == "mysql"


def ensure_sqlite_database() -> None:
    if using_mysql() or DB_PATH.exists():
        return

    from scripts.init_db import main as init_database

    init_database()


def normalize_value(value: Any) -> Any:
    if isinstance(value, (datetime, date)):
        return value.isoformat(sep=" ") if isinstance(value, datetime) else value.isoformat()

    return value


def row_to_dict(row: Any) -> dict:
    if isinstance(row, dict):
        return {key: normalize_value(value) for key, value in row.items()}

    return {key: normalize_value(row[key]) for key in row.keys()}


def get_connection():
    if using_mysql():
        try:
            import pymysql
        except ImportError as exc:
            raise RuntimeError("Falta PyMySQL. Ejecuta: py -m pip install -r requirements.txt") from exc

        return pymysql.connect(
            host=os.environ.get("DB_HOST", "127.0.0.1"),
            port=int(os.environ.get("DB_PORT", "3306")),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", ""),
            database=os.environ.get("DB_NAME", "miraflor"),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

    ensure_sqlite_database()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


class MiraflorHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        path = urlparse(self.path).path

        try:
            if path == "/api/health":
                self.check_database()
                self.send_json({"ok": True, "database": "mysql" if using_mysql() else "sqlite"})
                return

            if path == "/api/jugadores":
                self.send_json(self.fetch_all("SELECT * FROM jugadores ORDER BY dorsal"))
                return

            if path == "/api/partidos":
                self.send_json(self.fetch_all("SELECT * FROM partidos ORDER BY jornada"))
                return

            if path == "/api/inscripciones":
                self.send_json(self.fetch_all("SELECT * FROM inscripciones ORDER BY creada_en DESC"))
                return
        except Exception as exc:
            self.send_json({"ok": False, "error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)
            return

        super().do_GET()

    def do_POST(self) -> None:
        path = urlparse(self.path).path

        if path != "/api/inscripciones":
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        try:
            payload = self.read_json()
            missing = self.validate_inscription(payload)

            if missing:
                self.send_json({"ok": False, "error": "Faltan campos obligatorios", "missing": missing}, HTTPStatus.BAD_REQUEST)
                return

            inscription_id = self.insert_inscription(payload)
            self.send_json({"ok": True, "id": inscription_id}, HTTPStatus.CREATED)
        except Exception as exc:
            self.send_json({"ok": False, "error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def fetch_all(self, query: str) -> list[dict]:
        with get_connection() as conn:
            if using_mysql():
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    return [row_to_dict(row) for row in cursor.fetchall()]

            return [row_to_dict(row) for row in conn.execute(query).fetchall()]

    def check_database(self) -> None:
        with get_connection() as conn:
            if using_mysql():
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1 AS ok")
                    cursor.fetchone()
                return

            conn.execute("SELECT 1").fetchone()

    def validate_inscription(self, payload: dict) -> list[str]:
        required = [
            "nombre_alumno",
            "apellidos_alumno",
            "fecha_nacimiento",
            "categoria",
            "tutor",
            "telefono",
            "email",
        ]
        return [field for field in required if not payload.get(field)]

    def insert_inscription(self, payload: dict) -> int:
        placeholder = "%s" if using_mysql() else "?"
        values_sql = ", ".join([placeholder] * 10)
        query = f"""
            INSERT INTO inscripciones
            (nombre_alumno, apellidos_alumno, fecha_nacimiento, categoria, experiencia,
             tutor, telefono, email, observaciones, privacidad)
            VALUES ({values_sql})
        """
        values = (
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
        )

        with get_connection() as conn:
            if using_mysql():
                with conn.cursor() as cursor:
                    cursor.execute(query, values)
                    conn.commit()
                    return int(cursor.lastrowid)

            cursor = conn.execute(query, values)
            conn.commit()
            return int(cursor.lastrowid)

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
    ensure_sqlite_database()
    mimetypes.add_type("text/css", ".css")
    mimetypes.add_type("application/javascript", ".js")

    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))

    server = ThreadingHTTPServer((host, port), MiraflorHandler)
    print(f"Web Miraflor lista en http://{host}:{port}")
    print(f"Base de datos: {'MySQL' if using_mysql() else 'SQLite'}")
    print("API: /api/health, /api/jugadores, /api/partidos, /api/inscripciones")
    server.serve_forever()


if __name__ == "__main__":
    main()
