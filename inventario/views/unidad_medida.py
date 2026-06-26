from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from inventario.models import UnidadMedida
from inventario.serializers import UnidadMedidaSerializer

class UnidadMedidaViewSet(viewsets.ModelViewSet):
    queryset = UnidadMedida.objects.all()
    serializer_class = UnidadMedidaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['cantidad_por_unidad']
    search_fields = ['nombre']
    ordering_fields = ['id', 'nombre', 'cantidad_por_unidad']
    ordering = ['nombre']

    @action(detail=False, methods=['get'], url_path='multiples')
    def unidades_multiples(self, request):
        unidades = self.queryset.filter(cantidad_por_unidad__gt=1)
        page = self.paginate_queryset(unidades)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(unidades, many=True)
        return Response(serializer.data, status=status.HTTP_200_NOT_CONTENT)