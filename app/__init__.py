from flask import Flask
from config import Config
from .extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    @app.shell_context_processor
    def contexto_shell():
        return {
            "db": db,
            "Usuario": models.Usuario,
            "Cliente": models.Cliente,
            "Producto": models.Producto,
            "Venta": models.Venta,
            "DetalleVenta": models.DetalleVenta,
        }

    return app

app = create_app()