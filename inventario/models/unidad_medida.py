from django.db import models

class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=50, unique=True, help_text="Ej: Kilogramo, Unidad, Caja")
    abreviatura = models.CharField(max_length=10, unique=True, help_text="Ej: kg, un, cx")

    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'

    def __str__(self):
        return f"{self.nombre} ({self.abreviatura})"