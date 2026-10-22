from datetime import datetime, timezone
from decimal import Decimal
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default="vendedor")

    def set_password(self, plano):
        self.password = generate_password_hash(plano)

    def check_password(self, plano):
        return check_password_hash(self.password, plano)

    def __repr__(self):
        return f"<Usuario {self.username}>"


class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True)
    telefono = db.Column(db.String(20))

    # Relación inversa
    ventas = db.relationship("Venta", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente {self.nombre}>"


class Producto(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    
    # ✅ COLUMNA AGREGADA — PASO 11
    categoria = db.Column(db.String(50))  # nullable=True por defecto

    # Relación inversa
    detalles = db.relationship("DetalleVenta", back_populates="producto")

    def __repr__(self):
        return f"<Producto {self.descripcion}>"


class Venta(db.Model):
    __tablename__ = "ventas"
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(
        db.DateTime, nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)

    cliente = db.relationship("Cliente", back_populates="ventas")
    detalles = db.relationship(
        "DetalleVenta", back_populates="venta",
        cascade="all, delete-orphan"
    )

    @property
    def total(self):
        return sum(d.cantidad * d.precio_unitario for d in self.detalles)

    def __repr__(self):
        return f"<Venta {self.id}>"


class DetalleVenta(db.Model):
    __tablename__ = "detalle_ventas"
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey("ventas.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    venta = db.relationship("Venta", back_populates="detalles")
    producto = db.relationship("Producto", back_populates="detalles")

    def __repr__(self):
        return f"<DetalleVenta venta={self.venta_id} prod={self.producto_id}>"