from django.db import models
from .traslado_bodega import TrasladoBodega

class TrasladoBodegaDetalle(models.Model):
    traslado = models.ForeignKey(TrasladoBodega, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('inventario.Producto', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Detalle de Traslado'
        verbose_name_plural = 'Detalles de Traslados'

    def __str__(self):
        return f"{self.cantidad} - {self.producto}"