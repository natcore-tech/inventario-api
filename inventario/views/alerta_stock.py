from rest_framework import viewsets, permissions
from inventario.models import AlertaStockMinimo
from inventario.serializers.alerta_stock import AlertaStockMinimoSerializer

class AlertaStockMinimoViewSet(viewsets.ModelViewSet):
    queryset = AlertaStockMinimo.objects.all()
    serializer_class = AlertaStockMinimoSerializer
    permission_classes = [permissions.IsAuthenticated]