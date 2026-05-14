PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS jugadores (
  id INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL,
  posicion TEXT NOT NULL,
  dorsal INTEGER NOT NULL UNIQUE,
  edad INTEGER,
  altura TEXT,
  foto TEXT,
  descripcion TEXT
);

CREATE TABLE IF NOT EXISTS partidos (
  id INTEGER PRIMARY KEY,
  jornada INTEGER NOT NULL UNIQUE,
  fecha TEXT NOT NULL,
  local TEXT NOT NULL,
  visitante TEXT NOT NULL,
  goles_local INTEGER,
  goles_visitante INTEGER,
  estado TEXT NOT NULL CHECK (estado IN ('jugado', 'por_jugar')),
  competicion TEXT NOT NULL DEFAULT 'Preferente Madrid Grupo 4',
  temporada TEXT NOT NULL DEFAULT '2025/2026'
);

CREATE TABLE IF NOT EXISTS inscripciones (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre_alumno TEXT NOT NULL,
  apellidos_alumno TEXT NOT NULL,
  fecha_nacimiento TEXT NOT NULL,
  categoria TEXT NOT NULL,
  experiencia TEXT,
  tutor TEXT NOT NULL,
  telefono TEXT NOT NULL,
  email TEXT NOT NULL,
  observaciones TEXT,
  privacidad INTEGER NOT NULL DEFAULT 1,
  creada_en TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
