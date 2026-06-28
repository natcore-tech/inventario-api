from rest_framework import viewsets, permissions
from inventario.models.devolucion import DevolucionCliente
from inventario.serializers.devolucion import DevolucionClienteSerializer

class DevolucionClienteViewSet(viewsets.ModelViewSet):
    queryset = DevolucionCliente.objects.all()
    serializer_class = DevolucionClienteSerializer
    permission_classes = [permissions.IsAuthenticated]