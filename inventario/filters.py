# inventario/filters.py
import django_filters
from inventario.models import (
    Categoria, 
    Producto, 
    MovimientoInventario, 
    Proveedor, 
    OrdenCompra  
)


class FiltroCategoria(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model  = Categoria
        fields = ['activa']


class FiltroProducto(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    codigo_barras = django_filters.CharFilter(lookup_expr='exact')
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')
    stock_min = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    stock_max = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')
    
    nombre_categoria = django_filters.CharFilter(
        field_name='categoria__nombre', lookup_expr='icontains'
    )

    class Meta:
        model  = Producto
        fields = ['es_activo', 'categoria']


class FiltroMovimientoInventario(django_filters.FilterSet):
    fecha_desde = django_filters.DateTimeFilter(field_name='creado_en', lookup_expr='gte')
    fecha_hasta = django_filters.DateTimeFilter(field_name='creado_en', lookup_expr='lte')
    motivo = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = MovimientoInventario
        fields = ['tipo', 'producto', 'usuario', 'proveedor']


class FiltroProveedor(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')
    ruc    = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model  = Proveedor
        fields = ['es_activo']


class FiltroOrdenCompra(django_filters.FilterSet):
    codigo_orden = django_filters.CharFilter(lookup_expr='icontains')
    fecha_desde = django_filters.DateTimeFilter(field_name='creado_en', lookup_expr='gte')
    fecha_hasta = django_filters.DateTimeFilter(field_name='creado_en', lookup_expr='lte')

    class Meta:
        model = OrdenCompra
        fields = ['estado', 'proveedor', 'usuario']