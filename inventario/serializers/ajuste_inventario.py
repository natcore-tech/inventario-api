from rest_framework import serializers
from django.db import transaction
from inventario.models import AjusteInventario

class AjusteInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AjusteInventario
        fields = '__all__'

    def create(self, validated_data):
        with transaction.atomic():
            ajuste = AjusteInventario.objects.create(**validated_data)
            
 
            producto = ajuste.producto
            producto.stock += ajuste.cantidad
            producto.save()
            
        return ajuste