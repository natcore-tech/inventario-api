from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from inventario.views.cliente import ClienteViewSet
from inventario.views.health import health_check
from inventario.views.auth import RegisterView, LogoutView
from inventario.views.turno_caja import TurnoCajaViewSet
from inventario.views.user import UserViewSet
from inventario.views.categoria import CategoriaViewSet
from inventario.views.producto import ConjuntoVistasProducto
from inventario.views.movimiento_inventario import MovimientoInventarioViewSet 
from inventario.serializers.auth import CustomTokenView
from inventario.views.proveedor import ProveedorViewSet 
from inventario.views.orden_compra import OrdenCompraViewSet  
from inventario.views.cotizacion import CotizacionViewSet
from inventario.views.venta import VentaViewSet  
from inventario.views.marca import MarcaViewSet
from inventario.views.unidad_medida import UnidadMedidaViewSet
from inventario.views.ubicacion_fisica import UbicacionFisicaViewSet
from inventario.views.bodega import BodegaViewSet
from inventario.views.stock_bodega import StockBodegaViewSet
from inventario.views.traslado_bodega import TrasladoBodegaViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('categorias', CategoriaViewSet, basename='categoria')
router.register('productos', ConjuntoVistasProducto, basename='producto')
router.register('movimientos', MovimientoInventarioViewSet, basename='movimiento-inventario')  
router.register('proveedores', ProveedorViewSet, basename='proveedor')  
router.register('ordenes-compra', OrdenCompraViewSet, basename='orden-compra')
router.register('cotizaciones', CotizacionViewSet)  
router.register('turnos-caja', TurnoCajaViewSet, basename='turno-caja')  
router.register('ventas', VentaViewSet, basename='venta')
router.register('clientes', ClienteViewSet, basename='cliente')  
router.register('marcas', MarcaViewSet, basename='marca')
router.register('unidades-medida', UnidadMedidaViewSet, basename='unidad-medida')
router.register('ubicaciones', UbicacionFisicaViewSet, basename='ubicacion-fisica')
router.register('bodegas', BodegaViewSet, basename='bodega')
router.register('stocks-bodegas', StockBodegaViewSet, basename='stock-bodega')
router.register('traslados-bodegas', TrasladoBodegaViewSet, basename='traslado-bodega')

urlpatterns = [
    path('health/', health_check),
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/', TokenVerifyView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('', include(router.urls)),
]