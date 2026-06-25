# inventario/views/cliente.py
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from inventario.models import Cliente
from inventario.serializers import SerializerCliente

class ClienteViewSet(viewsets.ModelViewSet):

    queryset = Cliente.objects.all()
    serializer_class = SerializerCliente
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['nombre', 'email']
    ordering = ['nombre']
