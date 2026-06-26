from django.db import models
from inventario.models import Producto
from django.db.models.signals import post_save
from django.dispatch import receiver

class AlertaStockMinimo(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='alerta_stock')
    cantidad_minima = models.IntegerField(default=5, verbose_name="Stock Mínimo para Alerta")
    email_notificacion = models.EmailField(verbose_name="Correo para compras")
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = 'inventario_alerta_stock'

    def __str__(self):
        return f"Alerta para {self.producto.nombre} (Min: {self.cantidad_minima})"


@receiver(post_save, sender=Producto)
def check_stock_alerta(sender, instance, **kwargs):
    if hasattr(instance, 'alerta_stock'):
        alerta = instance.alerta_stock
        if alerta.activa and instance.stock <= alerta.cantidad_minima:
            print(f"ALERTA: El producto {instance.nombre} ha bajado de su stock mínimo. Nivel actual: {instance.stock}")