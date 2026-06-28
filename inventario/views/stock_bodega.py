from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from inventario.models import StockBodega
from inventario.serializers import StockBodegaSerializer

class StockBodegaViewSet(viewsets.ModelViewSet):
    queryset = StockBodega.objects.select_related('bodega', 'producto').all()
    serializer_class = StockBodegaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['bodega', 'producto']
    ordering_fields = ['cantidad']