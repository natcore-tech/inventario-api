from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class OrdenCompra(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente de Entrega'),
        ('RECIBIDA', 'Recibida Completamente'),
        ('CANCELADA', 'Cancelada'),
    ]

    proveedor = models.ForeignKey(
        'inventario.Proveedor',
        on_delete=models.PROTECT,
        related_name='ordenes_compra',
        verbose_name='Proveedor'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='ordenes_compra',
        verbose_name='Usuario Emisor'
    )

    productos = models.ManyToManyField(
        'inventario.Producto',
        through='OrdenCompraDetalle', 
        related_name='ordenes_compra',
        verbose_name='Productos Solicitados'
    )
    
    codigo_orden = models.CharField(max_length=20, unique=True, verbose_name='Código de Orden')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PENDIENTE', verbose_name='Estado')
    total_estimado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total ($)')
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Emisión')

    class Meta:
        db_table = 'inventario_orden_compra'
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Órdenes de Compra'
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.codigo_orden} - {self.proveedor.nombre} ({self.estado})"

class OrdenCompraDetalle(models.Model):
    orden_compra = models.ForeignKey(
        OrdenCompra, 
        on_delete=models.CASCADE, 
        related_name='detalles' 
    )
    producto = models.ForeignKey(
        'inventario.Producto', 
        on_delete=models.PROTECT
    )
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    precio_unitario_compra = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Precio de Compra'
    )

    class Meta:
        db_table = 'inventario_orden_compra_detalle'
        verbose_name = "Detalle de Orden de Compra"
        verbose_name_plural = "Detalles de Órdenes de Compra"

    def __str__(self):
        return f"{self.cantidad} unids. de {self.producto.nombre} (OC {self.orden_compra.codigo_orden})"