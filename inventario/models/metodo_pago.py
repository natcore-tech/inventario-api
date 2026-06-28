# inventario/models/metodo_pago.py
from django.db import models


class MetodoPago(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    es_activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventario_metodo_pago'
        verbose_name = "Método de Pago"
        verbose_name_plural = "Métodos de Pago"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre