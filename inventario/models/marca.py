from django.db import models

class Marca(models.Model):
    nombre = models.CharField(max_length=100, unique=True, help_text="Nombre comercial del fabricante")
    estado = models.BooleanField(default=True, help_text="Indica si la marca esta activa")

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.nombre