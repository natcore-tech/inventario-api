# inventario/views/metodo_pago.py
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from inventario.models import MetodoPago
from inventario.serializers.metodo_pago import MetodoPagoSerializer
from inventario.permissions import EsStaffOSoloLectura
from inventario.pagination import StandardPagination


class MetodoPagoViewSet(viewsets.ModelViewSet):
    queryset = MetodoPago.objects.all()
    serializer_class = MetodoPagoSerializer
    permission_classes = [EsStaffOSoloLectura]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['es_activo']
    search_fields = ['nombre']
    ordering_fields = ['nombre', 'creado_en']
    ordering = ['nombre']

    def perform_destroy(self, instance):
        # Soft delete para proteger historiales contables
        instance.es_activo = False
        instance.save()