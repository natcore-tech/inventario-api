# inventario/models/__init__.py
from .categoria import Categoria
from .producto import Producto 
from .movimiento_inventario import MovimientoInventario
from .proveedor import Proveedor
from .orden_compra import OrdenCompra, OrdenCompraDetalle
from .orden_compra import OrdenCompra
from .ajuste_inventario import 
from .numero_serie import 
from .alerta_stock import 
from .devolucion import DevolucionCliente
from .turno_caja import TurnoCaja
from .venta import Venta, VentaDetalle, PagoVenta
from .cliente import Cliente
from .marca import Marca
from .unidad_medida import UnidadMedida
from .ubicacion_fisica import UbicacionFisica
from .bodega import Bodega
from .stock_bodega import StockBodega
from .traslado_bodega import TrasladoBodega
from .traslado_bodega_detalle import TrasladoBodegaDetalle

__all__ = ['Categoria', 'Producto', 'MovimientoInventario', 
           'Proveedor', 'OrdenCompra', 'OrdenCompraDetalle',
           'Cotizacion', 'CotizacionDetalle',
           'TurnoCaja', 'Venta', 'VentaDetalle', 'PagoVenta',
           'AjusteInventario', 'NumeroSerie', 'AlertaStockMinimo',
           'DevolucionCliente', 'Bodega', 'StockBodega', 
           'TrasladoBodega', 'TrasladoBodegaDetalle']




