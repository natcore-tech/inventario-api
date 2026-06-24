# inventario/views/producto.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Max, Min, Sum, Count

from inventario.models import Producto
from inventario.serializers.producto import SerializerProducto, SerializerResumenProducto
from inventario.permissions import EsStaffOSoloLectura
from inventario.filters import FiltroProducto
from inventario.pagination import StandardPagination


class ConjuntoVistasProducto(viewsets.ModelViewSet):
    queryset           = Producto.objects.select_related('categoria').all()
    serializer_class   = SerializerProducto
    permission_classes = [EsStaffOSoloLectura]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = FiltroProducto
    search_fields      = ['nombre', 'descripcion', 'categoria__name']
    ordering_fields    = ['nombre', 'precio', 'stock', 'creado_en']
    ordering           = ['nombre']

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdminUser],
        url_path='reabastecer',
    )
    def reabastecer(self, request, pk=None):
        producto = self.get_object()
        try:
            quantity = int(request.data.get('quantity', 0))
            if quantity <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                {'error': 'La cantidad debe ser un número entero positivo.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        producto.stock += quantity
        producto.save(update_fields=['stock'])
        return Response({
            'id':         producto.id,
            'nombre':     producto.nombre,
            'nuevo_stock': producto.stock,
        })

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[AllowAny],
        url_path='disponibles',
    )
    def disponibles(self, request):
        qs   = self.filter_queryset(
            self.get_queryset().filter(stock__gt=0, es_activo=True)
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                SerializerResumenProducto(page, many=True).data
            )
        return Response(SerializerResumenProducto(qs, many=True).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='estadisticas',
    )
    def estadisticas(self, request):
        qs      = Producto.objects.all()
        active  = qs.filter(es_activo=True)
        data    = active.aggregate(
            total_activos  = Count('id'),
            precio_promedio = Avg('precio'),
            precio_maximo   = Max('precio'),
            precio_minimo   = Min('precio'),
            total_stock    = Sum('stock'),
        )
        data['total_inactivos'] = qs.filter(es_activo=False).count()
        data['sin_stock']       = active.filter(stock=0).count()
        if data['precio_promedio']:
            data['precio_promedio'] = round(float(data['precio_promedio']), 2)
        return Response(data)