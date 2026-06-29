from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from inventario.models import UnidadMedida
from inventario.serializers import UnidadMedidaSerializer


class UnidadMedidaViewSet(viewsets.ModelViewSet):
    queryset = UnidadMedida.objects.all()
    serializer_class = UnidadMedidaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtros reales basados estrictamente en tu modelo:
    filterset_fields = ['nombre', 'abreviatura']
    search_fields = ['nombre', 'abreviatura']
    ordering_fields = ['id', 'nombre', 'abreviatura']
    ordering = ['nombre']