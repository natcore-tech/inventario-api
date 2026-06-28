# inventario/models/turno_caja.py
from django.db import models
from django.conf import settings


class TurnoCaja(models.Model):
    ESTADOS = [
        ('ABIERTO', 'Abierto'),
        ('CERRADO', 'Cerrado'),
    ]

    cajero = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT,
        verbose_name="Cajero Responsable"
    )
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    monto_apertura = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Fondo inicial en caja"
    )
    monto_cierre = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name="Dinero contado al cerrar"
    )
    estado = models.CharField(max_length=15, choices=ESTADOS, default='ABIERTO')
    observaciones = models.TextField(blank=True, help_text="Justificación de sobrantes o faltantes")

    class Meta:
        db_table = 'inventario_turno_caja'
        verbose_name = "Turno de Caja"
        verbose_name_plural = "Turnos de Caja"
        ordering = ['-fecha_apertura']

    def __str__(self):
        return f"Turno #{self.id} - {self.cajero.username} ({self.estado})"
