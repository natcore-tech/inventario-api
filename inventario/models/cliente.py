# inventario/models/cliente.py
from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    cedula = models.CharField(max_length=10)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField(unique=True)

