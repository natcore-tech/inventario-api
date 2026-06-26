from django.db import models
from inventario.models import Producto

class AjusteInventario(models.Model):
    TIPO_CHOICES = [
        ('ROBO', 'Robo o Hurto'),
        ('DANO', 'Mercadería Dañada/Rota'),
        ('CADUCIDAD', 'Caducidad/Vencimiento'),
        ('ERROR', 'Error de Conteo'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='ajustes')
    tipo_ajuste = models.CharField(max_length=15, choices=TIPO_CHOICES)
    cantidad = models.IntegerField(help_text="Usa negativos para disminuir stock, positivos para aumentar")
    justificativo = models.TextField(verbose_name="Descripción o motivo legal")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventario_ajuste_inventario'
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.tipo_ajuste} - {self.producto.nombre} ({self.cantidad})"