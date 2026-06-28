from rest_framework import serializers
from inventario.models import OrdenCompra, OrdenCompraDetalle

# 1. Serializer para los detalles (la tabla intermedia)
class DetalleCompraSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = OrdenCompraDetalle
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'precio_costo']

# 2. Serializer principal para la Orden de Compra
class SerializerOrdenCompra(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    
    # Usamos source='ordencompradetalle_set' para acceder a los detalles vinculados
    detalles = DetalleCompraSerializer(source='ordencompradetalle_set', many=True, read_only=True)

    class Meta:
        model = OrdenCompra
        fields = [
            'id', 
            'codigo_orden', 
            'proveedor', 
            'proveedor_nombre', 
            'usuario', 
            'estado', 
            'estado_display', 
            'total_estimado', 
            'detalles', 
            'creado_en'
        ]
        # Si quieres que el usuario no pueda modificar el código_orden manualmente:
        read_only_fields = ['codigo_orden', 'creado_en', 'usuario']

    def validate_total_estimado(self, value):
        if value < 0:
            raise serializers.ValidationError("El total estimado no puede ser un valor negativo.")
        return value