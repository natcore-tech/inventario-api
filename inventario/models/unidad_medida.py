from django.db import models

class UnidadMedida(models.Model):
    # Ej: "Unidad", "Caja", "Par", "Kilogramo"
    nombre = models.CharField(max_length=50)
    
    # Ej: Para "Caja de 12", este valor sería 12. Para "Unidad", sería 1.
    cantidad_por_unidad = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'

    def __str__(self):
        if self.cantidad_por_unidad > 1:
            return f"{self.nombre} de {self.cantidad_por_unidad}"
        return self.nombre