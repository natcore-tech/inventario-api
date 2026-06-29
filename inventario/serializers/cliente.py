# inventario/serializers/cliente.py
from rest_framework import serializers
from inventario.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    total_compras = serializers.SerializerMethodField()

    class Meta:
        model = Cliente
        fields = [
            'id', 
            'identificacion', 
            'nombres', 
            'email', 
            'telefono', 
            'direccion', 
            'es_activo', 
            'total_compras',
            'creado_en', 
            'actualizado_en'
        ]
        read_only_fields = ['id', 'total_compras', 'creado_en', 'actualizado_en']

    def get_total_compras(self, obj) -> int:
        # Cuando exista el modelo Venta en la Tarea 4, contará automáticamente las facturas pagadas
        if hasattr(obj, 'venta_set'):
            return obj.venta_set.filter(estado='PAGADA').count()
        return 0

    def validate_identificacion(self, valor):
        identificacion = valor.strip()
        
        # 1. Validar longitud estándar en Ecuador
        if len(identificacion) not in [10, 13]:
            raise serializers.ValidationError(
                "La identificación debe tener exactamente 10 dígitos (Cédula) o 13 (RUC)."
            )

        # 2. Validar que sean solo números
        if not identificacion.isdigit():
            raise serializers.ValidationError("La identificación debe contener únicamente números.")

        # 3. Validar duplicados ignorando el propio registro al editar (PUT/PATCH)
        instancia = getattr(self, 'instance', None)
        consulta = Cliente.objects.filter(identificacion=identificacion)
        if instancia:
            consulta = consulta.exclude(pk=instancia.pk)

        if consulta.exists():
            raise serializers.ValidationError("Ya existe un cliente registrado con este número de cédula/RUC.")

        return identificacion

    def validate_nombres(self, valor):
        nombres = valor.strip()
        if len(nombres) < 3:
            raise serializers.ValidationError("El nombre del cliente es demasiado corto.")
        return nombres