from django.contrib import admin
from inventario.models import (
    Categoria, Producto, MovimientoInventario, Proveedor, OrdenCompra, 
    OrdenCompraDetalle, TurnoCaja, Venta, VentaDetalle, PagoVenta, Cliente, 
    MetodoPago, Promocion, AjusteInventario, NumeroSerie, AlertaStockMinimo, 
    DevolucionCliente, Bodega, StockBodega, TrasladoBodega, TrasladoBodegaDetalle, 
    Marca, UnidadMedida, UbicacionFisica, Cotizacion, CotizacionDetalle
)


@admin.register(Categoria)
class CategoryAdmin(admin.ModelAdmin):
    list_display        = ['id', 'nombre', 'slug', 'activa', 'creado_en']
    list_filter         = ['activa']
    search_fields       = ['nombre']
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombre', 'precio', 'stock', 'es_activo', 'categoria']
    list_filter   = ['es_activo', 'categoria']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'es_activo']


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display    = ['id', 'creado_en', 'tipo', 'producto', 'cantidad', 'proveedor', 'usuario']
    list_filter     = ['tipo', 'creado_en', 'usuario', 'proveedor']
    search_fields   = ['producto__nombre', 'motivo', 'proveedor__nombre']
    ordering        = ['-creado_en']
    readonly_fields = ['producto', 'tipo', 'cantidad', 'proveedor', 'usuario', 'creado_en']


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombre', 'ruc', 'telefono', 'es_activo', 'creado_en']
    list_filter   = ['es_activo', 'creado_en']
    search_fields = ['nombre', 'ruc']
    list_editable = ['es_activo']


class OrdenCompraDetalleInline(admin.TabularInline):
    model = OrdenCompraDetalle
    extra = 1  


@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display  = ['id', 'codigo_orden', 'proveedor', 'estado', 'total_estimado', 'usuario', 'creado_en']
    list_filter   = ['estado', 'creado_en', 'proveedor']
    search_fields = ['codigo_orden', 'proveedor__nombre']
    list_editable = ['estado']
    ordering      = ['-creado_en']
    inlines       = [OrdenCompraDetalleInline]


@admin.register(OrdenCompraDetalle)
class OrdenCompraDetalleAdmin(admin.ModelAdmin):
    list_display  = ['id', 'orden_compra', 'producto', 'cantidad', 'precio_unitario_compra']
    list_filter   = ['orden_compra']
    search_fields = ['producto__nombre', 'orden_compra__codigo_orden']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display    = ['id', 'nombres', 'identificacion', 'email', 'telefono', 'es_activo', 'creado_en']
    list_filter     = ['es_activo', 'creado_en']
    search_fields   = ['nombres', 'identificacion', 'email']
    list_editable   = ['es_activo']
    ordering        = ['nombres']
    readonly_fields = ['creado_en', 'actualizado_en']


@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombre', 'es_activo', 'creado_en']
    list_filter   = ['es_activo']
    search_fields = ['nombre']
    list_editable = ['es_activo']
    ordering      = ['nombre']


@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombre', 'producto', 'porcentaje_descuento', 'fecha_inicio', 'fecha_fin', 'es_activa']
    list_filter   = ['es_activa', 'fecha_inicio']
    search_fields = ['nombre', 'producto__nombre']
    list_editable = ['es_activa']
    ordering      = ['-fecha_inicio']


@admin.register(TurnoCaja)
class TurnoCajaAdmin(admin.ModelAdmin):
    list_display    = ['id', 'cajero', 'fecha_apertura', 'fecha_cierre', 'monto_apertura', 'estado']
    list_filter     = ['estado', 'cajero']
    search_fields   = ['cajero__username', 'id']
    ordering        = ['-fecha_apertura']
    readonly_fields = ['fecha_apertura', 'fecha_cierre']


class VentaDetalleInline(admin.TabularInline):
    model = VentaDetalle
    extra = 0
    readonly_fields = ['producto', 'cantidad', 'precio_unitario_venta', 'subtotal_linea']
    can_delete = False


class PagoVentaInline(admin.TabularInline):
    model = PagoVenta
    extra = 0
    readonly_fields = ['metodo_pago', 'monto', 'fecha_pago']
    can_delete = False


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display    = ['id', 'cliente', 'cajero', 'turno', 'fecha_emision', 'total', 'estado']
    list_filter     = ['estado', 'fecha_emision', 'cajero']
    search_fields   = ['cliente__nombres', 'cliente__identificacion', 'id']
    ordering        = ['-fecha_emision']
    inlines         = [VentaDetalleInline, PagoVentaInline]
    readonly_fields = ['subtotal', 'iva', 'total', 'fecha_emision', 'cajero', 'turno']


@admin.register(VentaDetalle)
class VentaDetalleAdmin(admin.ModelAdmin):
    list_display  = ['id', 'venta', 'producto', 'cantidad', 'subtotal_linea']
    list_filter   = ['producto']


@admin.register(PagoVenta)
class PagoVentaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'venta', 'metodo_pago', 'monto', 'fecha_pago']
    list_filter   = ['metodo_pago']


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombre']
    search_fields = ['nombre']
    ordering      = ['nombre']


@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombre', 'abreviatura']
    search_fields = ['nombre', 'abreviatura']
    ordering      = ['nombre']


@admin.register(UbicacionFisica)
class UbicacionFisicaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'pasillo', 'estante', 'nivel']
    search_fields = ['pasillo', 'estante']
    ordering      = ['pasillo', 'estante']


@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombre', 'activa']
    list_filter   = ['activa']
    search_fields = ['nombre']
    list_editable = ['activa']


@admin.register(StockBodega)
class StockBodegaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'bodega', 'producto', 'cantidad']
    list_filter   = ['bodega']
    search_fields = ['producto__nombre', 'bodega__nombre']
    list_editable = ['cantidad']


@admin.register(AjusteInventario)
class AjusteInventarioAdmin(admin.ModelAdmin):
    list_display  = ['id', 'producto', 'tipo_ajuste', 'cantidad', 'creado_en']
    list_filter   = ['tipo_ajuste', 'creado_en']
    search_fields = ['producto__nombre', 'justificativo']
    ordering      = ['-creado_en']


@admin.register(AlertaStockMinimo)
class AlertaStockMinimoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'email_notificacion', 'cantidad_minima', 'activa']
    list_filter   = ['activa']
    search_fields = ['email_notificacion']
    list_editable = ['activa', 'cantidad_minima']


@admin.register(NumeroSerie)
class NumeroSerieAdmin(admin.ModelAdmin):
    list_display  = ['id', 'producto', 'codigo_serial', 'estado', 'fecha_ingreso']
    list_filter   = ['estado', 'fecha_ingreso']
    search_fields = ['codigo_serial', 'producto__nombre']


class TrasladoBodegaDetalleInline(admin.TabularInline):
    model = TrasladoBodegaDetalle
    extra = 1


@admin.register(TrasladoBodega)
class TrasladoBodegaAdmin(admin.ModelAdmin):
    list_display  = ['id', 'bodega_origen', 'bodega_destino', 'fecha_traslado', 'estado']
    list_filter   = ['estado', 'fecha_traslado', 'bodega_origen']
    search_fields = ['id']
    ordering      = ['-fecha_traslado']
    inlines       = [TrasladoBodegaDetalleInline]


@admin.register(TrasladoBodegaDetalle)
class TrasladoBodegaDetalleAdmin(admin.ModelAdmin):
    list_display = ['id', 'traslado', 'producto', 'cantidad']


class CotizacionDetalleInline(admin.TabularInline):
    model = CotizacionDetalle
    extra = 1


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display  = ['id', 'codigo_cotizacion', 'proveedor', 'fecha_emision', 'total_propuesto']
    list_filter   = ['fecha_emision', 'proveedor']
    search_fields = ['codigo_cotizacion', 'proveedor__nombre']
    ordering      = ['-fecha_emision']
    inlines       = [CotizacionDetalleInline]


@admin.register(CotizacionDetalle)
class CotizacionDetalleAdmin(admin.ModelAdmin):
    list_display = ['id', 'cotizacion', 'producto', 'cantidad', 'precio_propuesto']


@admin.register(DevolucionCliente)
class DevolucionClienteAdmin(admin.ModelAdmin):
    list_display  = ['id', 'producto', 'cantidad', 'motivo', 'estado_producto', 'fecha_devolucion']
    list_filter   = ['estado_producto', 'fecha_devolucion']
    search_fields = ['producto__nombre', 'motivo']
    ordering      = ['-fecha_devolucion']