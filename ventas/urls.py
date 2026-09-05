from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/crear/', views.crear_pedido, name='crear_pedido'),
    path('pedidos/editar/<int:id>/', views.editar_pedido, name='editar_pedido'),
    path('pedidos/eliminar/<int:id>/', views.eliminar_pedido, name='eliminar_pedido'),

    path('detalles/', views.lista_detalles, name='lista_detalles'),
    path('detalles/crear/', views.crear_detalle, name='crear_detalle'),
    path('detalles/editar/<int:id>/', views.editar_detalle, name='editar_detalle'),
    path('detalles/eliminar/<int:id>/', views.eliminar_detalle, name='eliminar_detalle'),

    path('pagos/', views.lista_pagos, name='lista_pagos'),
    path('pagos/crear/', views.crear_pago, name='crear_pago'),
    path('pagos/editar/<int:id>/', views.editar_pago, name='editar_pago'),
    path('pagos/eliminar/<int:id>/', views.eliminar_pago, name='eliminar_pago'),

    path('envios/', views.lista_envios, name='lista_envios'),
    path('envios/crear/', views.crear_envio, name='crear_envio'),
    path('envios/editar/<int:id>/', views.editar_envio, name='editar_envio'),
    path('envios/eliminar/<int:id>/', views.eliminar_envio, name='eliminar_envio'),

    path('cupones/', views.lista_cupones, name='lista_cupones'),
    path('cupones/crear/', views.crear_cupon, name='crear_cupon'),
    path('cupones/editar/<int:id>/', views.editar_cupon, name='editar_cupon'),
    path('cupones/eliminar/<int:id>/', views.eliminar_cupon, name='eliminar_cupon'),
]