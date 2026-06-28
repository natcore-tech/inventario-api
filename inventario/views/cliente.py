# inventario/views/cliente.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from inventario.models import Cliente
from inventario.serializers.cliente import ClienteSerializer
from inventario.permissions import EsStaffOSoloLectura
from inventario.pagination import StandardPagination


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [EsStaffOSoloLectura]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['nombres', 'identificacion', 'email']
    ordering_fields = ['nombres', 'creado_en']
    ordering = ['nombres']

    def perform_destroy(self, instance):
        instance.es_activo = False
        instance.save()

    @action(detail=False, methods=['get'], url_path='estadisticas')
    def estadisticas(self, request):
        qs = Cliente.objects.all()
        return Response({
            'total': qs.count(),
            'activos': qs.filter(es_activo=True).count(),
            'inactivos': qs.filter(es_activo=False).count(),
        })