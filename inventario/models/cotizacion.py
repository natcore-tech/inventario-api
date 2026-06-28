from django.db import models
from inventario.models import Proveedor, Producto

class Cotizacion(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='cotizaciones')
    codigo_cotizacion = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    fecha_validez = models.DateField()
    total_propuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        db_table = 'inventario_cotizacion'

class CotizacionDetalle(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_propuesto = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'inventario_cotizacion_detalle'