from app.models.base_model import BaseModel
from app.models import db

class MovimientoStock(BaseModel):
    __tablename__ = 'movimientos_stock'
    
    tipo_movimiento = db.Column(db.String(10), nullable = False)    # 'entrada' o 'salida'
    cantidad = db.Column(db.Integer, nullable = False)
    motivo = db.Column(db.String(200), nullable = True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)  # Para registrar quién hizo el movimiento
    
    
    producto = db.relationship('Producto', back_populates='movimientos_stock')
    user= db.relationship('User')
    
    def __init__(self,tipo_movimiento, cantidad, motivo, producto_id, user_id) -> None:
        self.tipo_movimiento = tipo_movimiento
        self.cantidad = cantidad
        self.motivo = motivo
        self.producto_id = producto_id
        self.user_id = user_id

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'tipo_movimiento': self.tipo_movimiento,
            'cantidad': self.cantidad,
            'producto_id': self.producto_id,
            'motivo': self.motivo,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'activo' : self.activo
            
            
            
        })
        return data