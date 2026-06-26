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
from .marca import MarcaSerializer
from .unidad_medida import UnidadMedidaSerializer
from .ubicacion_fisica import UbicacionFisicaSerializer