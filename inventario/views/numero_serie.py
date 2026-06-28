from rest_framework import viewsets, permissions
from inventario.models import NumeroSerie
from inventario.serializers.numero_serie import NumeroSerieSerializer

class NumeroSerieViewSet(viewsets.ModelViewSet):
    queryset = NumeroSerie.objects.all()
    serializer_class = NumeroSerieSerializer
    permission_classes = [permissions.IsAuthenticated]