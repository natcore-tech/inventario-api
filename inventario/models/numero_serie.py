from django.db import models
from inventario.models import Producto

class NumeroSerie(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='numeros_serie')
    codigo_serial = models.CharField(max_length=100, unique=True, verbose_name="Número de Serie / IMEI")
    estado = models.CharField(
        max_length=20, 
        choices=[('DISPONIBLE', 'Disponible'), ('VENDIDO', 'Vendido'), ('DANO', 'Dañado')],
        default='DISPONIBLE'
    )
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventario_numero_serie'
        verbose_name = "Número de Serie"
        verbose_name_plural = "Números de Serie"

    def __str__(self):
        return f"{self.producto.nombre} - {self.codigo_serial}"