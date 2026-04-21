from typing import Literal
from app.models.producto import Producto
from sqlalchemy.exc import IntegrityError
from app.models.producto import Producto # es necesario importarla
from app.models.categoria import Categoria # es necesario importarla
from app.models.proveedor import Proveedor # es necesario importarla
from app.models.movimientos_stock import MovimientoStock # es necesario importarla
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller


class ProductoController (Controller):
    
    @staticmethod
    def get_all() -> tuple[Response, int]:
        productos_list = db.session.execute(db.select(Producto).order_by(db.desc(Producto.id))).scalars().all()
        if len(productos_list) > 0:
            productos_to_dict = [producto.to_dict() for producto in productos_list ]
            return jsonify(productos_to_dict), 200 
        return jsonify({"message": 'producto no encontrado'}), 404
    
    @staticmethod
    def show(id)->tuple[Response, int]:
        producto = db.session.get(Producto, id)
        if producto:
            return jsonify(producto.to_dict()), 200
        return jsonify({"message": 'producto no encontrado'}), 404
    
    @staticmethod
    def create(request) -> tuple[Response, int]:
        nombre:str = request.get['nombre']
        descripcion:str = request['descripcion']
        precio_costo:float = request.get['precio_costo']
        precio_venta:float = request.get['precio_venta']
        stock_actual:int = request['stock_actual']
        stock_minimo:int = request['stock_minimo']
        categoria_id:int = request.get['categoria_id']
        proveedor_id:int = request['proveedor_id']
        
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if descripcion is None:
            error = 'La descripción es requerida'
        if precio_costo is None:
            error = 'El precio de costo es requerido'
        if precio_venta is None:
            error = 'El precio de venta es requerido'
        if categoria_id is None:
            error = 'La categoria es requerida'
        if error is None:
            if stock_actual < 0:
                error = 'El stock actual no puede ser negativo'
            if stock_minimo < 0:
                error = 'El stock mínimo no puede ser negativo'
            try:
                producto = Producto(nombre=nombre, descripcion=descripcion, precio_costo=precio_costo, precio_venta=precio_venta, stock_actual=stock_actual, stock_minimo=stock_minimo, categoria_id=categoria_id, proveedor_id=proveedor_id)
                db.session.add(producto)
                db.session.commit()
                return jsonify({'message': "Producto creado con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': "Producto ya registrado"}), 409
        return jsonify ({'message': error}), 422
        
        
    @staticmethod
    def update(request, id)->tuple[Response, int]:
        nombre:str = request.get['nombre']
        descripcion:str = request['descripcion']
        precio_costo:float = request.get['precio_costo']
        precio_venta:float = request.get['precio_venta']
        stock_actual:int = request['stock_actual']
        stock_minimo:int = request['stock_minimo']
        categoria_id:int = request.get['categoria_id']
        proveedor_id:int = request['proveedor_id']
        
        error :str | None = None
        if nombre is None:
            error = 'El nombre es requerido'
        if precio_costo is None:
            error = 'El precio de costo es requerido'
        if precio_venta is None:
            error = 'El precio de venta es requerido'
        if categoria_id is None:
            error = 'La categoria es requerida'
        
                      
        if error is None:
            producto = db.session.get(Producto, id)
            if producto:
                try:
                    producto.nombre = nombre
                    producto.descripcion = descripcion
                    producto.precio_costo = precio_costo
                    producto.precio_venta = precio_venta
                    producto.stock_actual = stock_actual
                    producto.stock_minimo = stock_minimo 
                    producto.categoria_id = categoria_id
                    producto.proveedor_id = proveedor_id
                    db.session.commit()
                    return jsonify({'message':'producto modificado con exito'}), 200
                except IntegrityError:
                    db.session.rollback()
                    return jsonify({'message': "Producto ya registrado"}), 409
            # else:
            #         error = 'producto no encontrado'
                
        return jsonify({'message': error}), 422

    @staticmethod
    def destroy(id) -> tuple[Response, int]:
        producto = db.session.get(Producto, id)
        error = None
        if producto:
            db.session.delete(producto)
            db.session.commit()
            return jsonify({'message':'el producto fue eliminado con exito'}), 200
        else:
            error = 'Producto no encontrado'
        return jsonify({'message':error}), 422