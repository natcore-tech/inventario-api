from django.db import models

class UbicacionFisica(models.Model):
    # Ej: "Pasillo A", "Pasillo B"
    pasillo = models.CharField(max_length=20)
    
    # Ej: "Estante 4", "Estante 12"
    estante = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Ubicación Física'
        verbose_name_plural = 'Ubicaciones Físicas'

    def __str__(self):
        return f"{self.pasillo} - {self.estante}"