from django.db import models

class Marca(models.Model):
    # Aquí se guardarán valores como: "Lenovo", "Dell", "HP"
    nombre = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.nombre