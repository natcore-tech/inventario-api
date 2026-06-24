# inventario/serializers/orden_compra.py
from rest_framework import serializers
from inventario.models import OrdenCompra


class SerializerOrdenCompra(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    
    productos_detalles = serializers.SerializerMethodField()

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
            'productos',         
            'productos_detalles', 
            'creado_en'
        ]

    def get_productos_detalles(self, obj):
        """Devuelve una lista con los nombres y precios de los productos en la orden"""
        return [
            {
                "id": p.id,
                "nombre": p.nombre,
                "precio": str(p.precio)
            } for p in obj.productos.all()
        ]

    def validate_total_estimado(self, value):
        if value < 0:
            raise serializers.ValidationError("El total estimado no puede ser un valor negativo.")
        return value


SerializerOrdenCompra = SerializerOrdenCompra