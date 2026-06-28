# inventario/models/cliente.py
from django.db import models


class Cliente(models.Model):
    identificacion = models.CharField(
        max_length=13, 
        unique=True, 
        verbose_name="Cédula/RUC",
        help_text="10 dígitos para Cédula, 13 para RUC"
    )
    nombres = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    es_activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventario_cliente'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombres']

    def __str__(self):
        return f"{self.nombres} ({self.identificacion})"