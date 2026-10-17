import os
from datetime import timedelta
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()


def _uri_base_de_datos():
    """Prioridad: DATABASE_URL -> las 5 variables DB_* (Aiven) -> MySQL local de Docker."""
    if os.getenv('DATABASE_URL'):
        return os.environ['DATABASE_URL']
    if os.getenv('DB_HOST'):
        # URL.create escapa solo los caracteres raros de la contrasena (@, :, / ...)
        return URL.create(
            'mysql+pymysql',
            username=os.getenv('DB_USER', 'avnadmin'),
            password=os.getenv('DB_PASSWORD', ''),
            host=os.environ['DB_HOST'],
            port=int(os.getenv('DB_PORT', '3306')),
            database=os.getenv('DB_NAME', 'defaultdb'),
            query={'charset': 'utf8mb4'},
        )
    # MySQL local (contenedor Docker "yalpa", puerto 3308)
    return 'mysql+pymysql://root:12345678@localhost:3308/yalpa?charset=utf8mb4'


def _connect_args(uri, db_timezone):
    if not str(uri).startswith('mysql'):
        return {}
    args = {
        'init_command': f"SET time_zone='{db_timezone}'",
        # Aiven free puede estar apagado por inactividad: damos margen para que despierte
        'connect_timeout': int(os.getenv('DB_CONNECT_TIMEOUT', '15')),
    }
    # Aiven exige SSL. DB_SSL_CA = ruta al ca.pem descargado de Aiven (recomendado).
    # Sin ca.pem la conexion igual va cifrada, pero sin verificar el certificado.
    if os.getenv('DB_SSL_CA'):
        args['ssl'] = {'ca': os.environ['DB_SSL_CA']}
    elif os.getenv('DB_SSL', '0') == '1' or os.getenv('DB_HOST'):
        args['ssl'] = {'ssl': True}
    return args


class Config:
    SQLALCHEMY_DATABASE_URI = _uri_base_de_datos()
    SECRET_KEY = os.getenv('SECRET_KEY', 'yalpa_secret_key_2026')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Sesion de usuario (cookie firmada con SECRET_KEY)
    SESSION_COOKIE_HTTPONLY = True        # el JavaScript de la pagina no puede leer la cookie
    SESSION_COOKIE_SAMESITE = 'Lax'       # no se envia en peticiones POST desde otros sitios
    # Poner SESSION_COOKIE_SECURE=1 en produccion (HTTPS); en local con http:// debe quedar en 0
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', '0') == '1'
    PERMANENT_SESSION_LIFETIME = timedelta(days=int(os.getenv('SESSION_DAYS', '30')))

    # Zona horaria de la sesion MySQL (Peru = UTC-5) para que la hora de registro sea la real
    DB_TIMEZONE = os.getenv('DB_TIMEZONE', '-05:00')

    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,    # reconecta si MySQL cerro la conexion
        'pool_recycle': 280,
        'connect_args': _connect_args(SQLALCHEMY_DATABASE_URI, DB_TIMEZONE),
    }
