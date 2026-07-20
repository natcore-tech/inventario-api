# inventario/serializers/venta.py
from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from decimal import Decimal

from inventario.models import Venta, VentaDetalle, PagoVenta, TurnoCaja, Promocion


class VentaDetalleSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = VentaDetalle
        fields = ['id', 'producto', 'nombre_producto', 'cantidad', 'precio_unitario_venta', 'subtotal_linea']
        read_only_fields = ['id', 'nombre_producto', 'precio_unitario_venta', 'subtotal_linea']


class PagoVentaSerializer(serializers.ModelSerializer):
    nombre_metodo = serializers.CharField(source='metodo_pago.nombre', read_only=True)

    class Meta:
        model = PagoVenta
        fields = ['id', 'metodo_pago', 'nombre_metodo', 'monto', 'fecha_pago']
        read_only_fields = ['id', 'nombre_metodo', 'fecha_pago']


class VentaSerializer(serializers.ModelSerializer):
    detalles = VentaDetalleSerializer(many=True)
    pagos    = PagoVentaSerializer(many=True, required=False)
    nombre_cliente = serializers.CharField(source='cliente.nombres', read_only=True)
    nombre_cajero  = serializers.CharField(source='cajero.username', read_only=True)

    class Meta:
        model = Venta
        fields = [
            'id', 'cliente', 'nombre_cliente', 'cajero', 'nombre_cajero', 'turno',
            'fecha_emision', 'subtotal', 'iva', 'total', 'estado', 'detalles', 'pagos'
        ]
        read_only_fields = ['id', 'cajero', 'nombre_cajero', 'turno', 'fecha_emision', 'subtotal', 'iva', 'total', 'estado']

    def validate_detalles(self, valor):
        if not valor:
            raise serializers.ValidationError("La factura debe contener al menos un ítem.")
        return valor

    @transaction.atomic
    def create(self, datos_validados):
        detalles_data = datos_validados.pop('detalles')
        pagos_data    = datos_validados.pop('pagos', [])
        user          = self.context['request'].user

        # 1. SANITY CHECK: ¿Tiene caja abierta hoy?
        turno = TurnoCaja.objects.filter(cajero=user, estado='ABIERTO').first()
        if not turno:
            raise serializers.ValidationError("No puedes facturar porque no tienes un Turno de Caja abierto.")

        subtotal_acumulado = Decimal('0.00')
        detalles_a_crear   = []
        productos_a_restar = []
        hoy = timezone.now().date()

        # 2. PROCESAR CARRITO Y REVISAR BODEGAS
        for item in detalles_data:
            producto = item['producto']
            cantidad = item['cantidad']

            if producto.stock < cantidad:
                raise serializers.ValidationError(
                    f"Stock insuficiente para '{producto.nombre}'. Quedan {producto.stock} unidades."
                )

            # ¿Hay promoción activa hoy para este producto o para toda la tienda (NULL)?
            promo = Promocion.objects.filter(
                Q(producto=producto) | Q(producto__isnull=True),
                es_activa=True,
                fecha_inicio__lte=hoy,
                fecha_fin__gte=hoy
            ).order_by('-porcentaje_descuento').first()

            if promo:
                rebaja = promo.porcentaje_descuento / Decimal('100.00')
                precio_unit = producto.precio * (Decimal('1.00') - rebaja)
            else:
                precio_unit = producto.precio

            precio_unit    = round(precio_unit, 2)
            subtotal_linea = round(precio_unit * cantidad, 2)
            subtotal_acumulado += subtotal_linea

            producto.stock -= cantidad
            productos_a_restar.append(producto)

            detalles_a_crear.append({
                'producto': producto,
                'cantidad': cantidad,
                'precio_unitario_venta': precio_unit,
                'subtotal_linea': subtotal_linea
            })

        # 3. CÁLCULOS FISCALES (Ecuador IVA 15%)
        iva_calculado   = round(subtotal_acumulado * Decimal('0.15'), 2)
        total_calculado = subtotal_acumulado + iva_calculado

        # 4. CUADRE DE DINERO
        suma_pagos   = sum([p['monto'] for p in pagos_data], Decimal('0.00'))
        estado_venta = 'PAGADA' if suma_pagos >= total_calculado else 'EMITIDA'

        # 5. GUARDAR TRANSACCIÓN EN POSTGRES
        venta = Venta.objects.create(
            cliente=datos_validados['cliente'],
            cajero=user,
            turno=turno,
            subtotal=subtotal_acumulado,
            iva=iva_calculado,
            total=total_calculado,
            estado=estado_venta
        )

        for d in detalles_a_crear:
            VentaDetalle.objects.create(venta=venta, **d)

        for p in pagos_data:
            PagoVenta.objects.create(venta=venta, **p)

        for prod in productos_a_restar:
            prod.save() # Aquí se efectúa físicamente la resta del stock

        # Enviar correo de confirmación de forma silenciosa
        if venta.cliente.email:
            try:
                from inventario.services.email import send_venta_confirmation_email
                send_venta_confirmation_email(venta)
            except Exception as e:
                import logging
                logger = logging.getLogger(__name__)
                logger.exception('Error enviando confirmación de venta #%s', venta.id)

        return venta