from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Cliente CRUD
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('clientes/crear/', views.cliente_create, name='crear_cliente'),
    path('clientes/editar/', RedirectView.as_view(pattern_name='cliente_list', permanent=False)),
    path('clientes/<int:pk>/', views.cliente_detail, name='cliente_detail'),
    path('clientes/<int:pk>/editar/', views.cliente_update, name='editar_cliente'),
    path('clientes/<int:pk>/eliminar/', views.cliente_delete, name='eliminar_cliente'),

    # Listados de otras entidades
    path('metodos-pago/', views.metodo_pago_list, name='metodo_pago_list'),
    path('carritos/', views.carrito_list, name='carrito_list'),
    path('direcciones/', views.direccion_list, name='direccion_list'),
    path('resenas/', views.resena_list, name='resena_list'),

    #vistas con optimizacion de relaciones
    path('cliente/<int:pk>/perfil/', views.cliente_perfil_detail, name='cliente_perfil_detail'),
    path('cliente/<int:pk>/favoritos/', views.cliente_favoritos_list, name='cliente_favoritos_list'),

    path('favoritos/crear/', views.favorito_create, name='favorito_create'),
    path('favoritos/<int:pk>/editar/', views.favorito_update, name='favorito_update'),
    path('favoritos/<int:pk>/eliminar/', views.favorito_delete, name='favorito_delete'),
]
