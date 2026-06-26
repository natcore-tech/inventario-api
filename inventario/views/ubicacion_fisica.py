from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from inventario.models import UbicacionFisica
from inventario.serializers import UbicacionFisicaSerializer

class UbicacionFisicaViewSet(viewsets.ModelViewSet):
    queryset = UbicacionFisica.objects.all()
    serializer_class = UbicacionFisicaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['pasillo', 'estante']
    search_fields = ['pasillo', 'estante']
    ordering_fields = ['id', 'pasillo', 'estante']
    ordering = ['pasillo', 'estante']

    @action(detail=True, methods=['get'], url_path='disponibilidad')
    def verificar_disponibilidad(self, request, pk=None):
        ubicacion = self.get_object()
        tiene_productos = ubicacion.producto_set.exists() if hasattr(ubicacion, 'producto_set') else False
        return Response(
            {
                "ubicacion_id": ubicacion.id,
                "coordenada": f"{ubicacion.pasillo} - {ubicacion.estante}",
                "ocupada": tiene_productos
            },
            status=status.HTTP_200_OK
        )