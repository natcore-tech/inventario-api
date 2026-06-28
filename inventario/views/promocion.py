# inventario/views/promocion.py
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from inventario.models import Promocion
from inventario.serializers.promocion import PromocionSerializer
from inventario.permissions import EsStaffOSoloLectura
from inventario.pagination import StandardPagination


class PromocionViewSet(viewsets.ModelViewSet):
    queryset = Promocion.objects.all()
    serializer_class = PromocionSerializer
    permission_classes = [EsStaffOSoloLectura]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['es_activa', 'producto']
    search_fields = ['nombre', 'producto__nombre']
    ordering_fields = ['fecha_inicio', 'porcentaje_descuento']
    ordering = ['-fecha_inicio']