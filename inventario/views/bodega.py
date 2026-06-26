from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from inventario.models import Bodega, StockBodega
from inventario.serializers import BodegaSerializer, StockBodegaSerializer

class BodegaViewSet(viewsets.ModelViewSet):
    queryset = Bodega.objects.all()
    serializer_class = BodegaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['activa']
    search_fields = ['nombre', 'direccion']
    ordering_fields = ['nombre']
    ordering = ['nombre']

    @action(detail=True, methods=['get'], url_path='inventario')
    def inventario(self, request, pk=None):
        bodega = self.get_object()
        stock = StockBodega.objects.filter(bodega=bodega)
        serializer = StockBodegaSerializer(stock, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.stocks.filter(cantidad__gt=0).exists():
            return Response(
                {"error": "No se puede eliminar una bodega con stock disponible."},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)