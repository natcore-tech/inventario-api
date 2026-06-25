# inventario/serializers/cliente.py
from rest_framework import serializers
from inventario.models import Cliente

class SerializerCliente(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'cedula',
                   'telefono', 'correo']