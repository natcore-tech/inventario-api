from django.db import models
from .bodega import Bodega

class StockBodega(models.Model):
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='stocks')
    producto = models.ForeignKey('inventario.Producto', on_delete=models.CASCADE, related_name='stocks_bodega')
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Stock en Bodega'
        verbose_name_plural = 'Stocks en Bodegas'
        unique_together = ('bodega', 'producto')

    def __str__(self):
        return f"{self.producto} - {self.bodega.nombre}: {self.cantidad}"