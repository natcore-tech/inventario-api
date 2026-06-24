# inventario/views/proveedor.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from inventario.models import Proveedor
from inventario.serializers.proveedor import SerializerProveedor
from inventario.filters import FiltroProveedor


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = SerializerProveedor
    
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    
    filterset_class = FiltroProveedor
    
    ordering_fields = ['nombre', 'creado_en']
    ordering = ['nombre']