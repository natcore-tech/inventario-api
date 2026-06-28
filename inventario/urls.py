# inventario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

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
from inventario.views.venta import VentaViewSet  

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('categorias', CategoriaViewSet, basename='categoria')
router.register('productos', ConjuntoVistasProducto, basename='producto')
router.register('movimientos', MovimientoInventarioViewSet, basename='movimiento-inventario')  
router.register('proveedores', ProveedorViewSet, basename='proveedor')  
router.register('ordenes-compra', OrdenCompraViewSet, basename='orden-compra')
router.register('turnos-caja', TurnoCajaViewSet, basename='turno-caja')  
router.register('ventas', VentaViewSet, basename='venta')

urlpatterns = [
    path('health/', health_check),
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/', TokenVerifyView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('', include(router.urls)),
]