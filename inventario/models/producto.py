from django.db import models
from django.core.validators import MinValueValidator
from pathlib import Path
import uuid


def product_image_path(instance, filename):
    ext = Path(filename).suffix.lower()
    return f'products/{uuid.uuid4()}{ext}'

class Producto(models.Model):
    categoria = models.ForeignKey(
        'inventario.Categoria',
        on_delete=models.PROTECT,
        related_name='productos',
        verbose_name='Categoría'
    )
    nombre = models.CharField(
        max_length=150,
        verbose_name='Nombre del Producto'
    )
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )
    # Se eliminó 'max_length', no aplica en DecimalField
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Precio de Venta'
    )
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Stock Actual'
    )
    es_activo = models.BooleanField(
        default=True,
        verbose_name='¿Está Activo?'
    )
    creado_en = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    image = models.ImageField(
        upload_to=product_image_path, 
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'inventario_producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - Stock: {self.stock}"