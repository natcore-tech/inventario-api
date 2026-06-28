from rest_framework import serializers
from inventario.models import UbicacionFisica

class UbicacionFisicaSerializer(serializers.ModelSerializer):
    coordenada_exacta = serializers.SerializerMethodField()

    class Meta:
        model = UbicacionFisica
        fields = ['id', 'pasillo', 'estante', 'coordenada_exacta']
        read_only_fields = ['id', 'coordenada_exacta']

    def get_coordenada_exacta(self, obj):
        return f"{obj.pasillo} - {obj.estante}"

    def validate(self, data):
        pasillo = data.get('pasillo', '')
        estante = data.get('estante', '')
        
        if pasillo and not pasillo.strip():
            raise serializers.ValidationError({"pasillo": "El campo pasillo no puede estar compuesto solo por espacios."})
        
        if estante and not estante.strip():
            raise serializers.ValidationError({"estante": "El campo estante no puede estar compuesto solo por espacios."})
            
        return data

    def validate_pasillo(self, value):
        return value.strip().upper()

    def validate_estante(self, value):
        return value.strip().upper()