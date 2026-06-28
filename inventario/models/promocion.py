# inventario/models/promocion.py
from django.db import models


class Promocion(models.Model):
    nombre = models.CharField(max_length=150)
    producto = models.ForeignKey(
        'Producto', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        help_text="Valido solo para un producto a la vez."
    )
    porcentaje_descuento = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="Ejemplo: 15.00 equivale a un 15%"
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    es_activa = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventario_promocion'
        verbose_name = "Promoción"
        verbose_name_plural = "Promociones"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje_descuento}%)"