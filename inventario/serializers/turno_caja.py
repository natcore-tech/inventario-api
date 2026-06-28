# inventario/serializers/turno_caja.py
from rest_framework import serializers
from django.utils import timezone
from inventario.models import TurnoCaja


class TurnoCajaSerializer(serializers.ModelSerializer):
    nombre_cajero = serializers.CharField(source='cajero.username', read_only=True)

    class Meta:
        model = TurnoCaja
        fields = [
            'id',
            'cajero',
            'nombre_cajero',
            'fecha_apertura',
            'fecha_cierre',
            'monto_apertura',
            'monto_cierre',
            'estado',
            'observaciones'
        ]
        read_only_fields = ['id', 'cajero', 'nombre_cajero', 'fecha_apertura', 'fecha_cierre']

    def validate_monto_apertura(self, valor):
        if valor < 0:
            raise serializers.ValidationError("El monto de apertura no puede ser un número negativo.")
        return valor

    def validate(self, datos):
        request = self.context.get('request')
        if not request or not request.user:
            return datos

        # SI ESTÁ INTENTANDO ABRIR UN TURNO NUEVO (POST):
        if not self.instance:
            turno_abierto = TurnoCaja.objects.filter(cajero=request.user, estado='ABIERTO').exists()
            if turno_abierto:
                raise serializers.ValidationError(
                    "Ya tienes un turno de caja abierto actualmente. Debes cerrarlo antes de iniciar uno nuevo."
                )

        # SI ESTÁ CERRANDO LA CAJA (PUT/PATCH):
        nuevo_estado = datos.get('estado')
        if self.instance and self.instance.estado == 'ABIERTO' and nuevo_estado == 'CERRADO':
            if datos.get('monto_cierre') is None:
                raise serializers.ValidationError({
                    "monto_cierre": "Para cerrar la caja debes declarar obligatoriamente el dinero físico contado."
                })
            # Inyectamos la hora del servidor automáticamente tras bambalinas
            datos['fecha_cierre'] = timezone.now()

        return datos

    def create(self, datos_validados):
        # Asignar automáticamente el cajero logueado
        request = self.context.get('request')
        datos_validados['cajero'] = request.user
        return super().create(datos_validados)