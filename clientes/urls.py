from django.urls import path
from . import views

urlpatterns = [
    # Cliente CRUD
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/crear/', views.cliente_create, name='crear_cliente'),
    path('clientes/<int:pk>/', views.cliente_detail, name='cliente_detail'),
    path('clientes/<int:pk>/editar/', views.cliente_update, name='editar_cliente'),
    path('clientes/<int:pk>/eliminar/', views.cliente_delete, name='eliminar_cliente'),

    # Listados de otras entidades
    path('metodos-pago/', views.metodo_pago_list, name='metodo_pago_list'),
    path('carritos/', views.carrito_list, name='carrito_list'),
    path('direcciones/', views.direccion_list, name='direccion_list'),
    path('resenas/', views.resena_list, name='resena_list'),
]
