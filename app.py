import os

from sqlalchemy import text
from werkzeug.middleware.proxy_fix import ProxyFix

from app import create_app
from app.database import db

app = create_app()

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)


def probar_conexion():
    """Prueba rapida de la base de datos (paso 5 del manual de Flask y MySQL)."""
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            print('Conexión a la base de datos exitosa')
        except Exception as e:
            print('Fallo en la conexión a la base de datos')
            print(f'Detalle: {type(e).__name__}: {str(e)[:200]}')


if __name__ == "__main__":
    probar_conexion()

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
