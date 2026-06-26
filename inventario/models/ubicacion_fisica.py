from django.db import models

class UbicacionFisica(models.Model):
    pasillo = models.CharField(max_length=50, help_text="Ej: Pasillo A")
    estante = models.CharField(max_length=50, help_text="Ej: Estante 4")
    nivel = models.CharField(max_length=50, blank=True, null=True, help_text="Opcional. Ej: Nivel 2")

    class Meta:
        verbose_name = 'Ubicación Fisica'
        verbose_name_plural = 'Ubicaciones Fisicas'

    def __str__(self):
        return f"{self.pasillo} - {self.estante}"