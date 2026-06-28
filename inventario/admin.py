from django.contrib import admin
from inventario.models import (
    Categoria, 
    Producto, 
    MovimientoInventario, 
    Proveedor, 
    OrdenCompra,
    OrdenCompraDetalle,  
    TurnoCaja,
    Venta,
    VentaDetalle,
    PagoVenta,
    Cliente  
)



@admin.register(Categoria)
class CategoryAdmin(admin.ModelAdmin):
    list_display          = ['id', 'nombre', 'slug', 'activa', 'creado_en']
    list_filter           = ['activa']
    search_fields         = ['nombre']
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombre', 'precio', 'stock', 'es_activo', 'categoria']
    list_filter   = ['es_activo', 'categoria']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'es_activo']


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'creado_en', 'tipo', 'producto', 'cantidad', 'proveedor', 'usuario']
    list_filter = ['tipo', 'creado_en', 'usuario', 'proveedor']
    search_fields = ['producto__nombre', 'motivo', 'proveedor__nombre']
    ordering = ['-creado_en']
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
    
    inlines = [OrdenCompraDetalleInline]

@admin.register(TurnoCaja)
class TurnoCajaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cajero', 'fecha_apertura', 'fecha_cierre', 'monto_apertura', 'estado']
    list_filter  = ['estado', 'cajero']
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
    list_display  = ['id', 'cliente', 'cajero', 'turno', 'fecha_emision', 'total', 'estado']
    list_filter   = ['estado', 'fecha_emision', 'cajero']
    search_fields = ['cliente__nombres', 'cliente__identificacion', 'id']
    inlines       = [VentaDetalleInline, PagoVentaInline]
    readonly_fields = ['subtotal', 'iva', 'total', 'fecha_emision', 'cajero', 'turno']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombres', 'identificacion', 'email', 'telefono', 'es_activo', 'creado_en']
    list_filter   = ['es_activo', 'creado_en']
    search_fields = ['nombres', 'identificacion', 'email']
    list_editable = ['es_activo']
    ordering      = ['nombres']
    readonly_fields = ['creado_en', 'actualizado_en']
