# inventario/views/turno_caja.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from inventario.models import TurnoCaja
from inventario.serializers.turno_caja import TurnoCajaSerializer
from inventario.pagination import StandardPagination


class TurnoCajaViewSet(viewsets.ModelViewSet):
    serializer_class = TurnoCajaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['estado', 'cajero']
    ordering_fields = ['fecha_apertura']
    ordering = ['-fecha_apertura']

    def get_queryset(self):
        user = self.request.user
        # Filtro de seguridad: El staff/admin ve todo, el empleado común solo ve sus propios registros
        if user.is_staff:
            return TurnoCaja.objects.all()
        return TurnoCaja.objects.filter(cajero=user)