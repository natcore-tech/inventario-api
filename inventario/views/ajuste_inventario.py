from rest_framework import viewsets, permissions
from inventario.models import AjusteInventario
from inventario.serializers.ajuste_inventario import AjusteInventarioSerializer

class AjusteInventarioViewSet(viewsets.ModelViewSet):
    queryset = AjusteInventario.objects.all()
    serializer_class = AjusteInventarioSerializer
    permission_classes = [permissions.IsAuthenticated]