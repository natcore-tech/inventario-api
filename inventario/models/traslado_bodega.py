from django.db import models
from .bodega import Bodega

class TrasladoBodega(models.Model):
    fecha_traslado = models.DateTimeField(auto_now_add=True)
    bodega_origen = models.ForeignKey(Bodega, on_delete=models.PROTECT, related_name='traslados_salientes')
    bodega_destino = models.ForeignKey(Bodega, on_delete=models.PROTECT, related_name='traslados_entrantes')
    estado = models.CharField(
        max_length=20, 
        choices=[('EN_TRANSITO', 'En Tránsito'), ('COMPLETADO', 'Completado'), ('CANCELADO', 'Cancelado')], 
        default='EN_TRANSITO'
    )

    class Meta:
        verbose_name = 'Traslado de Bodega'
        verbose_name_plural = 'Traslados de Bodegas'

    def __str__(self):
        return f"Traslado {self.id}"