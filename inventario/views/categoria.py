# inventario/views/categoria.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from inventario.models import Categoria
from inventario.serializers.categoria import CategoriaSerializer
from inventario.permissions import EsStaffOSoloLectura
from inventario.filters import FiltroCategoria
from inventario.pagination import StandardPagination


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [EsStaffOSoloLectura]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FiltroCategoria
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'creado_en']
    ordering = ['nombre']

    @action(detail=True, methods=['get'], url_path='productos')
    def productos(self, request, pk=None):
        from inventario.models import Producto
        from inventario.serializers.producto import SerializadorResumenProducto
        
        category = self.get_object()
        qs   = category.products.filter(es_activo=True).order_by('nombre')
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                SerializadorResumenProducto(page, many=True).data
            )
        return Response(SerializadorResumenProducto(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='estadisticas')
    def estadisticas(self, request):
        qs = Categoria.objects.annotate(num_productos=Count('products', distinct=True))

        return Response({
            'total': qs.count(),
            'activas': qs.filter(activa=True).count(),
            'inactivas': qs.filter(activa=False).count(),
            'detalle': [
                {
                    'id': c.id,
                    'nombre': c.nombre,
                    'num_productos': c.num_productos,
                    'activa': c.activa,
                }
                for c in qs.order_by('nombre')
            ],
        })