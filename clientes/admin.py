from django.contrib import admin
from .models import Cliente, PerfilCliente, Direccion, Favorito

admin.site.register(Cliente)
admin.site.register(PerfilCliente)
admin.site.register(Direccion)
admin.site.register(Favorito)