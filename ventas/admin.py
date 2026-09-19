from django.contrib import admin

# Register your models here.
from .models import Pedido, DetallePedido, Pago, Envio

admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Pago)
admin.site.register(Envio)