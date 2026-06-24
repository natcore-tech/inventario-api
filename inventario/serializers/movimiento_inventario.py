# inventario/serializers/movimiento_inventario.py
from rest_framework import serializers
from inventario.models import MovimientoInventario


class SerializerMovimientoInventario(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    producto_categoria = serializers.CharField(source='producto.categoria.nombre', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)

    class Meta:
        model = MovimientoInventario
        fields = [
            'id', 
            'producto', 
            'producto_nombre', 
            'producto_categoria',
            'proveedor',         
            'proveedor_nombre',  
            'tipo', 
            'tipo_display', 
            'cantidad', 
            'motivo', 
            'usuario',
            'creado_en'
        ]

    def validate(self, data):
       
        if data.get('tipo') == 'ENTRADA' and not data.get('proveedor'):
            raise serializers.ValidationError({
                "proveedor": "El proveedor es requerido para los movimientos de tipo Entrada."
            })
        
        if data.get('tipo') != 'ENTRADA':
            data['proveedor'] = None
            
        return data