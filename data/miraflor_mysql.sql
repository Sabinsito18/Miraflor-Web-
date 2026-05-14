-- Base de datos A.C.D. Miraflor para MySQL
-- Generado desde data/miraflor.sqlite3
CREATE DATABASE IF NOT EXISTS `miraflor` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `miraflor`;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `inscripciones`;
DROP TABLE IF EXISTS `partidos`;
DROP TABLE IF EXISTS `jugadores`;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `jugadores` (
  `id` INT NOT NULL,
  `nombre` VARCHAR(120) NOT NULL,
  `posicion` VARCHAR(60) NOT NULL,
  `dorsal` INT NOT NULL,
  `edad` INT NULL,
  `altura` VARCHAR(20) NULL,
  `foto` VARCHAR(255) NULL,
  `descripcion` TEXT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_jugadores_dorsal` (`dorsal`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `partidos` (
  `id` INT NOT NULL,
  `jornada` INT NOT NULL,
  `fecha` DATETIME NOT NULL,
  `local` VARCHAR(160) NOT NULL,
  `visitante` VARCHAR(160) NOT NULL,
  `goles_local` INT NULL,
  `goles_visitante` INT NULL,
  `estado` ENUM('jugado', 'por_jugar') NOT NULL,
  `competicion` VARCHAR(160) NOT NULL DEFAULT 'Preferente Madrid Grupo 4',
  `temporada` VARCHAR(20) NOT NULL DEFAULT '2025/2026',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_partidos_jornada` (`jornada`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `inscripciones` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre_alumno` VARCHAR(120) NOT NULL,
  `apellidos_alumno` VARCHAR(160) NOT NULL,
  `fecha_nacimiento` DATE NOT NULL,
  `categoria` VARCHAR(60) NOT NULL,
  `experiencia` VARCHAR(120) NULL,
  `tutor` VARCHAR(180) NOT NULL,
  `telefono` VARCHAR(40) NOT NULL,
  `email` VARCHAR(180) NOT NULL,
  `observaciones` TEXT NULL,
  `privacidad` TINYINT(1) NOT NULL DEFAULT 1,
  `creada_en` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `jugadores` (`id`, `nombre`, `posicion`, `dorsal`, `edad`, `altura`, `foto`, `descripcion`) VALUES (1, 'Juan Perez', 'Portero', 1, 24, '1.85m', '/img/portero.png', 'Especialista en penaltis y gran reflejo bajo palos.');
INSERT INTO `jugadores` (`id`, `nombre`, `posicion`, `dorsal`, `edad`, `altura`, `foto`, `descripcion`) VALUES (2, 'Carlos Martin', 'Defensa', 4, 23, '1.80m', '/img/portero.png', 'Central contundente y seguro en el juego aereo.');
INSERT INTO `jugadores` (`id`, `nombre`, `posicion`, `dorsal`, `edad`, `altura`, `foto`, `descripcion`) VALUES (3, 'David Lopez', 'Centrocampista', 8, 25, '1.76m', '/img/portero.png', 'Organiza el juego y marca el ritmo del equipo.');
INSERT INTO `jugadores` (`id`, `nombre`, `posicion`, `dorsal`, `edad`, `altura`, `foto`, `descripcion`) VALUES (4, 'Miguel Sanchez', 'Delantero', 9, 22, '1.82m', '/img/portero.png', 'Referencia ofensiva con buen remate dentro del area.');
INSERT INTO `jugadores` (`id`, `nombre`, `posicion`, `dorsal`, `edad`, `altura`, `foto`, `descripcion`) VALUES (5, 'Alvaro Garcia', 'Extremo', 11, 21, '1.74m', '/img/portero.png', 'Jugador rapido, vertical y con desborde.');

INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (1, 1, '2025-09-14 11:00', 'Municipal Arroyomolinos', 'Cultural Deportiva Miraflor', 5, 0, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (2, 2, '2025-09-21 11:00', 'Cultural Deportiva Miraflor', 'CD Grinon B', 1, 0, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (3, 3, '2025-09-28 17:00', 'Villa del Prado', 'Cultural Deportiva Miraflor', 4, 3, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (4, 4, '2025-10-05 18:30', 'Cultural Deportiva Miraflor', 'Mostoles CF', 1, 1, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (5, 5, '2025-10-12 16:00', 'EF At. Casarrubuelos', 'Cultural Deportiva Miraflor', 3, 0, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (6, 6, '2025-10-19 17:00', 'Cultural Deportiva Miraflor', 'Union FC', 2, 1, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (7, 7, '2025-10-26 11:00', 'Lucero-Linces', 'Cultural Deportiva Miraflor', 3, 4, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (8, 8, '2025-11-02 17:00', 'Cultural Deportiva Miraflor', 'Humanes', 2, 1, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (9, 9, '2025-11-09 16:30', 'Atletico Valdeiglesias', 'Cultural Deportiva Miraflor', 3, 0, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (10, 10, '2025-11-16 17:00', 'Cultural Deportiva Miraflor', 'UD Mostoles Balompie', 2, 2, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (11, 11, '2025-11-23 12:15', 'Amistad Alcorcon A', 'Cultural Deportiva Miraflor', 2, 1, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (12, 12, '2025-11-30 17:00', 'Cultural Deportiva Miraflor', 'Fepe Getafe III', 3, 1, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (13, 13, '2025-12-14 12:00', 'Nuevo Boadilla', 'Cultural Deportiva Miraflor', 2, 2, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (14, 14, '2025-12-21 19:30', 'Cultural Deportiva Miraflor', 'Ciudad de Getafe SC', 0, 2, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (15, 15, '2026-01-11 17:00', 'Cultural Deportiva Miraflor', 'Leganes C', 2, 0, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (16, 16, '2026-01-18 11:15', 'CD Los Yebenes-San Bruno', 'Cultural Deportiva Miraflor', 4, 2, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (17, 17, '2026-01-25 17:00', 'Cultural Deportiva Miraflor', 'Moraleja de Enmedio', 2, 3, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (18, 18, '2026-02-01 17:00', 'Cultural Deportiva Miraflor', 'Municipal Arroyomolinos', 0, 6, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (19, 19, '2026-02-08 11:30', 'CD Grinon B', 'Cultural Deportiva Miraflor', 5, 3, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (20, 20, '2026-02-15 17:00', 'Cultural Deportiva Miraflor', 'Villa del Prado', 2, 3, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (21, 21, '2026-02-22 13:15', 'Mostoles CF', 'Cultural Deportiva Miraflor', 2, 0, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (22, 22, '2026-03-01 17:00', 'Cultural Deportiva Miraflor', 'EF At. Casarrubuelos', 3, 0, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (23, 23, '2026-03-08 15:00', 'Union FC', 'Cultural Deportiva Miraflor', 1, 1, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (24, 24, '2026-03-15 17:00', 'Cultural Deportiva Miraflor', 'Lucero-Linces', 1, 2, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (25, 25, '2026-03-22 12:00', 'Humanes', 'Cultural Deportiva Miraflor', 1, 0, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (26, 26, '2026-03-29 17:00', 'Cultural Deportiva Miraflor', 'Atletico Valdeiglesias', 3, 2, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (27, 27, '2026-04-12 17:30', 'UD Mostoles Balompie', 'Cultural Deportiva Miraflor', 5, 0, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (28, 28, '2026-04-19 17:00', 'Cultural Deportiva Miraflor', 'Amistad Alcorcon A', 2, 2, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (29, 29, '2026-04-26 16:00', 'Fepe Getafe III', 'Cultural Deportiva Miraflor', 2, 0, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (30, 30, '2026-05-10 17:00', 'Cultural Deportiva Miraflor', 'Nuevo Boadilla', 1, 2, 'jugado', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (31, 31, '2026-05-17 18:00', 'Ciudad de Getafe SC', 'Cultural Deportiva Miraflor', NULL, NULL, 'por_jugar', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (32, 32, '2026-05-24 00:00', 'Leganes C', 'Cultural Deportiva Miraflor', NULL, NULL, 'por_jugar', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (33, 33, '2026-05-31 00:00', 'Cultural Deportiva Miraflor', 'CD Los Yebenes-San Bruno', NULL, NULL, 'por_jugar', 'Preferente Madrid Grupo 4', '2025/2026');
INSERT INTO `partidos` (`id`, `jornada`, `fecha`, `local`, `visitante`, `goles_local`, `goles_visitante`, `estado`, `competicion`, `temporada`) VALUES (34, 34, '2026-06-07 00:00', 'Moraleja de Enmedio', 'Cultural Deportiva Miraflor', NULL, NULL, 'por_jugar', 'Preferente Madrid Grupo 4', '2025/2026');

-- Fin del volcado MySQL