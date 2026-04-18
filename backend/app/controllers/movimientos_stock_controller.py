from app.controllers.producto_controller import ProductoController
from app.models.movimientos_stock import MovimientoStock
from sqlalchemy.exc import IntegrityError
from app.models.producto import Producto 
from app.models.movimientos_stock import MovimientoStock 
from app.models import db
from flask import Response, jsonify
from app.controllers import Controller

class MovimientoStockController (Controller):
    
    @staticmethod
    def get_all() -> tuple[Response, int]:
        movimientos_list = db.session.execute(db.select(MovimientoStock).order_by(db.desc(MovimientoStock.id))).scalars().all()
        if len(movimientos_list) > 0:
            movimientos_to_dict = [movimiento.to_dict() for movimiento in movimientos_list ]
            return jsonify(movimientos_to_dict), 200 
        return jsonify({"message": 'movimientos de stock no encontrados'}), 404         
    
    @staticmethod
    def show(id)->tuple[Response, int]:
        movimiento = db.session.get(MovimientoStock, id)
        if movimiento:
            return jsonify(movimiento.to_dict()), 200
        return jsonify({"message": 'movimiento no encontrado'}), 404
    
    @staticmethod
    def create(request) -> tuple[Response, int]:
        tipo_movimiento:str = request.get['tipo_movimiento']
        cantidad:int = request.get['cantidad']
        motivo:str = request['motivo']
        producto_id:int = request.get['producto_id']
        user_id:int = request['user_id']
        
        error :str | None = None
        if tipo_movimiento is None:
            error = 'El tipo de movimiento es requerido'
        if cantidad is None:
            error = 'La cantidad es requerida'
        if producto_id is None:
            error = 'El producto es requerido'
        
        if error is None:
            if tipo_movimiento not in ['entrada', 'salida']:
                error = 'El tipo de movimiento debe ser "entrada" o "salida"'
            elif cantidad <= 0:
                error = 'La cantidad debe ser mayor a cero'
            else:
                producto:Producto | None = db.session.get(Producto, producto_id)
                if producto is None:
                    error = 'Producto no encontrado'
                elif tipo_movimiento == 'salida' and producto.stock_actual < cantidad:
                    error = 'No hay suficiente stock para realizar la salida'
        
        if error is None:
            try:
                movimiento_stock = MovimientoStock(tipo_movimiento=tipo_movimiento, cantidad=cantidad, motivo=motivo, producto_id=producto_id, user_id=user_id)
                db.session.add(movimiento_stock)
                
                # Actualizar el stock del producto
                if tipo_movimiento == 'entrada':
                    producto.stock_actual += cantidad
                else:  # salida
                    producto.stock_actual -= cantidad
                db.session.commit()
                return jsonify({'message': "Movimiento de stock registrado con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({'message': "Error al registrar el movimiento de stock"}), 409
        return jsonify ({'message': error}), 422
    
  
    def destroy(id) -> tuple[Response, int]:
        movimiento = db.session.get(MovimientoStock, id)
        if movimiento:
            producto:Producto | None = db.session.get(Producto, movimiento.producto_id)
            if producto:
                # Revertir el stock del producto antes de eliminar el movimiento
                if movimiento.tipo_movimiento == 'entrada':
                    producto.stock_actual -= movimiento.cantidad
                else:  # salida
                    producto.stock_actual += movimiento.cantidad
            db.session.delete(movimiento)
            db.session.commit()
            return jsonify({'message': 'Movimiento de stock eliminado con exito'}), 200
        return jsonify({"message": 'Movimiento de stock no encontrado'}), 404