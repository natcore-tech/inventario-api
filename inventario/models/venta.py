# inventario/models/venta.py
from django.db import models
from django.conf import settings


class Venta(models.Model):
    ESTADOS = [
        ('EMITIDA', 'Emitida'),
        ('PAGADA', 'Pagada'),
        ('ANULADA', 'Anulada'),
    ]

    cliente = models.ForeignKey('Cliente', on_delete=models.PROTECT)
    cajero = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    turno = models.ForeignKey('TurnoCaja', on_delete=models.PROTECT, related_name='ventas')
    fecha_emision = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='EMITIDA')

    class Meta:
        db_table = 'inventario_venta'
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha_emision']

    def __str__(self):
        return f"Venta #{self.id} - {self.cliente}"


class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('Producto', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario_venta = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_linea = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'inventario_venta_detalle'
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Venta"

    def __str__(self):
        return f"{self.cantidad}x {self.producto}"


class PagoVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='pagos')
    metodo_pago = models.ForeignKey('MetodoPago', on_delete=models.PROTECT)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pago = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventario_pago_venta'
        verbose_name = "Pago de Venta"
        verbose_name_plural = "Pagos de Ventas"

    def __str__(self):
        return f"${self.monto} en {self.metodo_pago}"