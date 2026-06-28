# inventario/models/__init__.py
from .categoria import Categoria
from .proveedor import Proveedor
from .cliente import Cliente
from .metodo_pago import MetodoPago

from .producto import Producto 
from .turno_caja import TurnoCaja
from .orden_compra import OrdenCompra
from .venta import Venta

from .orden_compra import OrdenCompraDetalle
from .ajuste_inventario import AjusteInventario
from .numero_serie import NumeroSerie
from .alerta_stock import AlertaStockMinimo
from .devolucion import DevolucionCliente
from .venta import VentaDetalle, PagoVenta
from .movimiento_inventario import MovimientoInventario
from .promocion import Promocion
from .marca import Marca
from .unidad_medida import UnidadMedida
from .ubicacion_fisica import UbicacionFisica
from .bodega import Bodega
from .stock_bodega import StockBodega
from .traslado_bodega import TrasladoBodega
from .traslado_bodega_detalle import TrasladoBodegaDetalle
from .cotizacion import Cotizacion, CotizacionDetalle

__all__ = ['Categoria', 'Producto', 'MovimientoInventario', 
           'Proveedor', 'OrdenCompra', 'OrdenCompraDetalle',
           'MetodoPago', 'Cotizacion', 'CotizacionDetalle',
           'TurnoCaja', 'Venta', 'VentaDetalle', 'PagoVenta',
           'AjusteInventario', 'NumeroSerie', 'AlertaStockMinimo',
           'DevolucionCliente', 'Bodega', 'StockBodega', 
           'TrasladoBodega', 'TrasladoBodegaDetalle',
           'Promocion', 'Cliente', 'Marca', 'UnidadMedida',
           'UbicacionFisica',]




