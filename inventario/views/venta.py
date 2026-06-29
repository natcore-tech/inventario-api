# inventario/view/venta.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from inventario.models import Venta
from inventario.serializers.venta import VentaSerializer
from inventario.pagination import StandardPagination


class VentaViewSet(viewsets.ModelViewSet):
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['estado', 'cliente', 'cajero', 'turno']
    ordering_fields = ['fecha_emision', 'total']
    ordering = ['-fecha_emision']

    def get_queryset(self):
        user = self.request.user
        
        if getattr(self, "swagger_fake_view", False):
            return Venta.objects.none()
        
        if user.is_staff:
            return Venta.objects.all()
        return Venta.objects.filter(cajero=user)