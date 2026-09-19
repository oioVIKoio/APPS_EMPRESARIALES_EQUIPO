from django.contrib import admin
from .models import Cliente, PerfilCliente, Direccion, Favorito


class PerfilClienteInline(admin.StackedInline):
	model = PerfilCliente
	extra = 0
	max_num = 1


class FavoritoInline(admin.TabularInline):
	model = Favorito
	extra = 0
	fields = ('producto', 'fecha_agregado', 'notificar_oferta')
	readonly_fields = ('fecha_agregado',)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
	list_display = ('id_cliente', 'nombre', 'apellido', 'email', 'telefono', 'fecha_registro')
	search_fields = ('nombre', 'apellido', 'email')
	list_filter = ('fecha_registro',)
	inlines = [PerfilClienteInline, FavoritoInline]


@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
	list_display = ('id_direccion', 'cliente', 'calle', 'ciudad', 'codigo_postal')
	search_fields = ('cliente__nombre', 'cliente__apellido', 'ciudad', 'codigo_postal')


admin.site.register(PerfilCliente)
admin.site.register(Favorito)