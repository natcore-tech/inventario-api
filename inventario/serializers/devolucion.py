from rest_framework import serializers
from inventario.models.devolucion import DevolucionCliente

class DevolucionClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevolucionCliente
        fields = '__all__'