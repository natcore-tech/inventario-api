from django.db import models
from inventario.models import Producto
from django.db.models.signals import post_save
from django.dispatch import receiver

class DevolucionCliente(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='devoluciones')
    fecha_devolucion = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(verbose_name="Motivo de la devolución")
    cantidad = models.IntegerField(default=1)
    estado_producto = models.CharField(
        max_length=20,
        choices=[('BUENO', 'Buen Estado'), ('DANO', 'Dañado'), ('USADO', 'Usado')],
        default='BUENO'
    )

    class Meta:
        db_table = 'inventario_devolucion_cliente'
        verbose_name = "Devolución de Cliente"
        verbose_name_plural = "Devoluciones de Clientes"

    def __str__(self):
        return f"Devolución: {self.producto.nombre} ({self.cantidad} un.)"

@receiver(post_save, sender=DevolucionCliente)
def reingresar_stock_por_devolucion(sender, instance, created, **kwargs):
    if created:
        if instance.estado_producto == 'BUENO':
            producto = instance.producto
            producto.stock += instance.cantidad
            producto.save()
            print(f"REINGRESO: {instance.cantidad} unidades de {producto.nombre} han vuelto al stock.")