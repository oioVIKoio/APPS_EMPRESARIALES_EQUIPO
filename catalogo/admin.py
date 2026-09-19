from django.contrib import admin

# Register your models here.
from .models import Categoria, Marca, Proveedor, Producto, Inventario

admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Inventario)