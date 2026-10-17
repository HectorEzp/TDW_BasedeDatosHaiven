from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import db

# Se ejecuta al arrancar (igual que DDL_CONTACTOS): la tabla se crea sola si no existe.
# El indice UNIQUE sobre "correo" garantiza una cuenta por correo aun si dos registros
# llegan a la vez. La collation utf8mb4_unicode_ci no distingue mayusculas.
DDL_USUARIOS = '''
CREATE TABLE IF NOT EXISTS usuarios (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_usuarios_correo (correo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
'''


class Usuario(db.Model):
    """Cuenta de cliente de la tienda (registro + inicio de sesion)."""
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    correo = db.Column(db.String(255), nullable=False, unique=True)
    telefono = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    creado_en = db.Column(db.TIMESTAMP, nullable=False, server_default=func.current_timestamp())

    def set_password(self, password):
        # Hash con sal (scrypt de Werkzeug): la contrasena nunca se guarda en claro.
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def primer_nombre(self):
        partes = self.nombre.split()
        return partes[0] if partes else self.nombre

    @property
    def iniciales(self):
        partes = self.nombre.split()
        return ''.join(p[0] for p in partes[:2]).upper() or '?'

    def __repr__(self):
        return f'<Usuario {self.id} {self.correo}>'
