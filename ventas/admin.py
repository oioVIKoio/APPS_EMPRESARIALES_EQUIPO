from django.contrib import admin

from .models import Cupon, DetallePedido, Envio, Pago, Pedido


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0


class PagoInline(admin.StackedInline):
    model = Pago
    extra = 0
    max_num = 1


class EnvioInline(admin.StackedInline):
    model = Envio
    extra = 0
    max_num = 1


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id_pedido', 'cliente', 'fecha_pedido', 'estado', 'total')
    search_fields = ('=id_pedido', 'cliente__nombre', 'cliente__apellido', 'cliente__email')
    list_filter = ('estado', 'fecha_pedido')
    list_select_related = ('cliente',)
    ordering = ('-fecha_pedido',)
    readonly_fields = ('fecha_pedido',)
    inlines = (DetallePedidoInline, PagoInline, EnvioInline)


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ('id_detalle', 'pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    search_fields = ('=pedido__id_pedido', 'producto__nombre', 'pedido__cliente__email')
    list_select_related = ('pedido__cliente', 'producto')
    ordering = ('-id_detalle',)


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id_pago', 'pedido', 'metodo_pago', 'monto', 'estado', 'fecha_pago')
    search_fields = ('=pedido__id_pedido', 'pedido__cliente__email', 'metodo_pago__tipo')
    list_filter = ('estado', 'metodo_pago')
    list_select_related = ('pedido__cliente', 'metodo_pago')
    ordering = ('-id_pago',)


@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    list_display = ('id_envio', 'pedido', 'direccion', 'empresa_envio', 'estado')
    search_fields = ('=pedido__id_pedido', 'pedido__cliente__email', 'empresa_envio', 'direccion__ciudad')
    list_filter = ('estado', 'empresa_envio')
    list_select_related = ('pedido__cliente', 'direccion__cliente')
    ordering = ('-id_envio',)


@admin.register(Cupon)
class CuponAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descuento', 'fecha_inicio', 'fecha_fin', 'activo')
    search_fields = ('codigo',)
    list_filter = ('activo',)
