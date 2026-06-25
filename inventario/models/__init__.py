# inventario/models/__init__.py
from .categoria import Categoria
from .producto import Producto 
from .movimiento_inventario import MovimientoInventario
from .proveedor import Proveedor
from .orden_compra import OrdenCompra
from .cliente import Cliente

__all__ = ['Categoria', 'Producto', 'MovimientoInventario', 'Proveedor', 'OrdenCompra', 'Cliente']