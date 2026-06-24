# inventario/models/proveedor.py
from django.db import models


class Proveedor(models.Model):
    nombre      = models.CharField(max_length=150)
    ruc         = models.CharField(max_length=13, unique=True)
    telefono    = models.CharField(max_length=20, blank=True, default='')
    email       = models.EmailField(blank=True, default='')
    direccion   = models.TextField(blank=True, default='')
    es_activo   = models.BooleanField(default=True)
    creado_en   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.ruc})"