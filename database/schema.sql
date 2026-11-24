CREATE DATABASE IF NOT EXISTS utp_matricula_s16 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE utp_matricula_s16;
CREATE TABLE IF NOT EXISTS cursos (
 id BIGINT PRIMARY KEY AUTO_INCREMENT,
 codigo VARCHAR(24) NOT NULL UNIQUE,
 nombre VARCHAR(150) NOT NULL,
 ciclo INT NOT NULL CHECK (ciclo BETWEEN 1 AND 10),
 vacantes INT NOT NULL CHECK (vacantes >= 0),
 INDEX idx_ciclo_vacantes (ciclo, vacantes), INDEX idx_nombre(nombre), INDEX idx_vacantes(vacantes)
) ENGINE=InnoDB;
INSERT IGNORE INTO cursos(id,codigo,nombre,ciclo,vacantes) VALUES
 (1,'100000S154','Desarrollo Web Integrado',6,30),
 (2,'100000S153','Base de Datos Avanzada',6,24),
 (3,'100000S152','Ingeniería de Software',6,18),
 (4,'100000S151','Redes y Comunicaciones',6,35),
 (5,'100000S150','Algoritmos y Estructuras de Datos',4,28),
 (6,'100000S149','Programación Orientada a Objetos',4,16),
 (7,'100000S148','Seguridad Informática',8,12),
 (8,'100000S147','Proyecto Integrador',8,0);
