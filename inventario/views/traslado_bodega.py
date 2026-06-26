from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from inventario.models import TrasladoBodega, StockBodega
from inventario.serializers import TrasladoBodegaSerializer

class TrasladoBodegaViewSet(viewsets.ModelViewSet):
    queryset = TrasladoBodega.objects.select_related('bodega_origen', 'bodega_destino').prefetch_related('detalles__producto').all()
    serializer_class = TrasladoBodegaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'bodega_origen', 'bodega_destino']
    ordering_fields = ['fecha_traslado']
    ordering = ['-fecha_traslado']

    @action(detail=True, methods=['post'], url_path='completar')
    @transaction.atomic
    def completar_traslado(self, request, pk=None):
        traslado = self.get_object()
        
        if traslado.estado != 'EN_TRANSITO':
            return Response(
                {"error": "Solo se pueden completar traslados en tránsito."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        for detalle in traslado.detalles.all():
            stock_origen = StockBodega.objects.filter(
                bodega=traslado.bodega_origen, 
                producto=detalle.producto
            ).first()

            if not stock_origen or stock_origen.cantidad < detalle.cantidad:
                return Response(
                    {"error": f"Stock insuficiente del producto {detalle.producto.id} en la bodega de origen."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            stock_origen.cantidad -= detalle.cantidad
            stock_origen.save()

            stock_destino, created = StockBodega.objects.get_or_create(
                bodega=traslado.bodega_destino,
                producto=detalle.producto,
                defaults={'cantidad': 0}
            )
            stock_destino.cantidad += detalle.cantidad
            stock_destino.save()

        traslado.estado = 'COMPLETADO'
        traslado.save()
        
        return Response({"status": "Traslado completado y stock actualizado."}, status=status.HTTP_200_OK)