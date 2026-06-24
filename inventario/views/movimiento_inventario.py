# inventario/views/movimiento_inventario.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from inventario.models import MovimientoInventario
from inventario.serializers import SerializerMovimientoInventario
from inventario.filters import FiltroMovimientoInventario


class MovimientoInventarioViewSet(viewsets.ModelViewSet):
    queryset = MovimientoInventario.objects.select_related(
        'producto', 'usuario', 'proveedor'
    ).all()
    serializer_class = SerializerMovimientoInventario
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(usuario=self.request.user)
        else:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Debes estar autenticado para registrar movimientos.")