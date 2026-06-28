# inventario/admin.py
from django.contrib import admin
from inventario.models import (
    Categoria, 
    Producto, 
    MovimientoInventario, 
    Proveedor, 
    OrdenCompra,
    Cliente  
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

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display  = ['id', 'codigo_orden', 'proveedor', 'estado', 'total_estimado', 'usuario', 'creado_en']
    list_filter   = ['estado', 'creado_en', 'proveedor']
    search_fields = ['codigo_orden', 'proveedor__nombre']
    list_editable = ['estado']
    ordering      = ['-creado_en']
    
    filter_horizontal = ['productos']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombres', 'identificacion', 'email', 'telefono', 'es_activo', 'creado_en']
    list_filter   = ['es_activo', 'creado_en']
    search_fields = ['nombres', 'identificacion', 'email']
    list_editable = ['es_activo']
    ordering      = ['nombres']
    readonly_fields = ['creado_en', 'actualizado_en']