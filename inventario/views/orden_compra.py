# inventario/views/orden_compra.py
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from inventario.models import OrdenCompra
from inventario.serializers import SerializerOrdenCompra
from inventario.filters import FiltroOrdenCompra


class OrdenCompraViewSet(viewsets.ModelViewSet):
  
    queryset = OrdenCompra.objects.all()
    serializer_class = SerializerOrdenCompra
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FiltroOrdenCompra
    ordering_fields = ['creado_en', 'total_estimado']
    ordering = ['-creado_en']

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)