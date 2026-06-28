from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db import transaction 

from inventario.models import OrdenCompra, OrdenCompraDetalle
from inventario.serializers.orden_compra import SerializerOrdenCompra
from inventario.filters import FiltroOrdenCompra

class OrdenCompraViewSet(viewsets.ModelViewSet):
    queryset = OrdenCompra.objects.all()
    serializer_class = SerializerOrdenCompra
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FiltroOrdenCompra
    ordering_fields = ['creado_en', 'total_estimado']
    ordering = ['-creado_en']

    def create(self, request, *args, **kwargs):
        detalles_data = request.data.get('detalles', [])
        
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            orden = serializer.save(usuario=self.request.user)
            
            for detalle in detalles_data:
                OrdenCompraDetalle.objects.create(
                    orden_compra=orden,
                    producto_id=detalle['producto'], 
                    cantidad=detalle['cantidad'],
                    precio_unitario_compra=detalle['precio_unitario_compra']
                )
            
            headers = self.get_success_headers(serializer.data)
            return Response(self.get_serializer(orden).data, status=status.HTTP_201_CREATED, headers=headers)