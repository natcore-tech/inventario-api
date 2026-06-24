# inventario/serializers/proveedor.py
from rest_framework import serializers
from inventario.models import Proveedor


class SerializerProveedor(serializers.ModelSerializer):
    class Meta:
        model  = Proveedor
        fields = [
            'id', 
            'nombre', 
            'ruc', 
            'telefono', 
            'email', 
            'direccion', 
            'es_activo', 
            'creado_en'
        ]