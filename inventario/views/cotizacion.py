from rest_framework import viewsets, permissions
from inventario.models import Cotizacion
from inventario.serializers.cotizacion import CotizacionSerializer

class CotizacionViewSet(viewsets.ModelViewSet):
    queryset = Cotizacion.objects.all()
    serializer_class = CotizacionSerializer
    permission_classes = [permissions.IsAuthenticated]