# inventario/models/categoria.py
from django.db import models


class Categoria(models.Model):
    nombre      = models.CharField(max_length=100, unique=True)
    slug        = models.SlugField(unique=True)
    descripcion = models.TextField(blank=True, default='')
    activa      = models.BooleanField(default=True)
    creado_en   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre