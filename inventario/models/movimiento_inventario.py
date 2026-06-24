# inventario/models/movimiento_inventario.py
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

# 🪓 ELIMINAMOS las importaciones directas para evitar bucles circulares infinitos

User = get_user_model()

class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('ENTRADA', 'Entrada (Compra/Ingreso)'),
        ('SALIDA', 'Salida (Venta/Egreso)'),
        ('AJUSTE_POS', 'Ajuste Positivo'),
        ('AJUSTE_NEG', 'Ajuste Negativo'),
    ]

    producto = models.ForeignKey(
        'inventario.Producto',
        on_delete=models.CASCADE,
        related_name='movimientos',
        verbose_name='Producto'
    )
    proveedor = models.ForeignKey(
        'inventario.Proveedor',
        on_delete=models.PROTECT,
        related_name='movimientos',
        null=True,
        blank=True,
        verbose_name='Proveedor'
    )
    tipo = models.CharField(
        max_length=15,
        choices=TIPO_MOVIMIENTO_CHOICES,
        verbose_name='Tipo de Movimiento'
    )
    cantidad = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Cantidad'
    )
    motivo = models.TextField(
        blank=True,
        null=True,
        help_text='Razón del movimiento (ej. Factura #123, rotura de stock, etc.)',
        verbose_name='Motivo/Detalle'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='movimientos_inventario',
        verbose_name='Usuario Responsable'
    )
    creado_en = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha del Movimiento'
    )

    class Meta:
        db_table = 'inventario_movimiento_inventario' 
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None
        
        if es_nuevo:
            producto = self.producto
            if self.tipo in ['ENTRADA', 'AJUSTE_POS']:
                producto.stock += self.cantidad
            elif self.tipo in ['SALIDA', 'AJUSTE_NEG']:
                if producto.stock < self.cantidad:
                    raise ValueError(
                        f"Stock insuficiente para {producto.nombre}. "
                        f"Disponible: {producto.stock}, Solicitado: {self.cantidad}"
                    )
                producto.stock -= self.cantidad
            
            producto.save(update_fields=['stock'])

        super().save(*args, **kwargs)