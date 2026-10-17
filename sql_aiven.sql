-- Para correr en Database Client (VS Code) sobre defaultdb y ver las tablas.
-- La app tambien las crea sola al arrancar (CREATE TABLE IF NOT EXISTS).

CREATE TABLE IF NOT EXISTS usuarios (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_usuarios_correo (correo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS contactos (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(150) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    telefono VARCHAR(20) NULL,
    asunto VARCHAR(100) NOT NULL DEFAULT 'Consultas generales',
    mensaje TEXT NOT NULL,
    leido TINYINT(1) NOT NULL DEFAULT 0,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha DATE GENERATED ALWAYS AS (DATE(creado_en)) STORED,
    hora TIME GENERATED ALWAYS AS (TIME(creado_en)) STORED,
    INDEX idx_correo (correo),
    INDEX idx_creado_en (creado_en)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SELECT id, nombre, correo, telefono, password_hash, creado_en FROM usuarios;
SELECT * FROM contactos;
