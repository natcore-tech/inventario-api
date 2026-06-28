# inventario/serializers/__init__.py
from .auth import CustomTokenSerializer, CustomTokenView
from .user import (
    RegisterSerializer,
    UserSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)
from .categoria import CategoriaSerializer
from .producto  import SerializerResumenProducto, SerializerProducto
from .movimiento_inventario import SerializerMovimientoInventario
from .proveedor import SerializerProveedor
from .orden_compra import SerializerOrdenCompra
from .turno_caja import TurnoCajaSerializer
from .venta import VentaSerializer
from .cliente import SerializerCliente
from .marca import MarcaSerializer
from .unidad_medida import UnidadMedidaSerializer
from .ubicacion_fisica import UbicacionFisicaSerializer
from .bodega import BodegaSerializer
from .stock_bodega import StockBodegaSerializer
from .traslado_bodega_detalle import TrasladoBodegaDetalleSerializer
from .traslado_bodega import TrasladoBodegaSerializer
