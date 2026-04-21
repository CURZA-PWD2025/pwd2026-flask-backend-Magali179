# from flask_sqlalchemy import SQLAlchemy
# from app.models.user import User
# from app.models.rol import Rol
# from app.models import db
# from flask import Flask
# from app import create_app

# app = create_app()


# def seed():
#     # Crear roles
#     admin_role = Rol(nombre='superadmin')
#     user_role = Rol(nombre='user')
#     db.session.add_all([admin_role, user_role])
#     db.session.commit()

#     # Crear usuarios
#     admin_user = User(nombre='admin', password='admin123', rol_id=admin_role.id, email='admin@example.com')
#     regular_user = User(nombre='user', password='user123', rol_id=user_role.id, email='user@example.com')
#     db.session.add_all([admin_user, regular_user])
#     db.session.commit()

    
# if __name__ == '__main__':
#     with app.app_context():
#         seed()

# seed.py
from app import create_app
from app.models import db
from app.models.rol import Rol
from app.models.user import User
from app.models.categoria import Categoria
from app.models.proveedor import Proveedor
from app.models.producto import Producto

app = create_app()

with app.app_context():
    # Roles
    rol_admin = Rol.query.filter_by(nombre='admin').first()
    if not rol_admin:
        rol_admin = Rol(nombre='admin')
        db.session.add(rol_admin)

    rol_op = Rol.query.filter_by(nombre='operador').first()
    if not rol_op:
        rol_op = Rol(nombre='operador')
        db.session.add(rol_op)
    db.session.commit()

    # Usuario admin
    rol_admin = Rol.query.filter_by(nombre='admin').first()
    if not rol_admin:
        rol_admin = Rol(nombre='admin')
        db.session.add(rol_admin)

    rol_op = Rol.query.filter_by(nombre='operador').first()
    if not rol_op:
        rol_op = Rol(nombre='operador')
        db.session.add(rol_op)
    db.session.commit()

    # Categorías
    alm = Categoria.query.filter_by(nombre='Almacén').first()
    if not alm:
        alm = Categoria(nombre='Almacén', descripcion='Productos secos')
        db.session.add(alm)

    lim = Categoria.query.filter_by(nombre='Limpieza').first()
    if not lim:
        lim = Categoria(nombre='Limpieza', descripcion='Artículos de limpieza')
        db.session.add(lim)

    db.session.commit()

    # Proveedor
    prov = Proveedor(nombre='Distribuidora Norte', contacto='Juan Pérez', telefono='2994001234', email='info@distribuidora-norte.com')
    db.session.add(prov)
    db.session.commit()

    # Productos
    db.session.add_all([
        Producto(nombre='Harina 000', descripcion='Harina de trigo 000', precio_costo=280, precio_venta=350,
                 stock_actual=50, stock_minimo=10,
                 categoria_id=alm.id, proveedor_id=prov.id),
        Producto(nombre='Lavandina 1L', descripcion='Lavandina de 1 litro', precio_costo=150, precio_venta=210,
                 stock_actual=30, stock_minimo=5,
                 categoria_id=lim.id, proveedor_id=prov.id),
    ])
    db.session.commit()
    print("Seed completado.")