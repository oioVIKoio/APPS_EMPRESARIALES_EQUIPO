from django.contrib import admin

from .models import Categoria, Inventario, Marca, Producto, Proveedor


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email')
    search_fields = ('nombre', 'email')
    ordering = ('nombre',)


class InventarioInline(admin.StackedInline):
    model = Inventario
    extra = 0
    max_num = 1


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'marca', 'proveedor', 'precio', 'fecha_registro')
    search_fields = ('nombre', 'categoria__nombre', 'marca__nombre', 'proveedor__nombre')
    list_filter = ('categoria', 'marca', 'proveedor')
    list_select_related = ('categoria', 'marca', 'proveedor')
    ordering = ('nombre',)
    readonly_fields = ('fecha_registro',)
    inlines = (InventarioInline,)


@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'cantidad', 'stock_minimo')
    search_fields = ('producto__nombre',)
    list_select_related = ('producto',)
    ordering = ('producto__nombre',)
