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

    # Ejercicio 3: Operación transaccional con atomic() y F()
    path('favoritos/<int:pk>/comprar/', views.comprar_favorito_confirm, name='comprar_favorito_confirm'),
    path('favoritos/<int:pk>/comprar/procesar/', views.comprar_favorito_procesar, name='comprar_favorito_procesar'),

    # Ejercicio 6: Página de reporte con floatformat
    path('reporte/', views.reporte_view, name='reporte_view'),

    # Ejercicio 7: QuerySet personalizado con as_manager
    path('favoritos/activos/', views.favoritos_activos_view, name='favoritos_activos_view'),
    path('favoritos/alto-valor/<int:umbral>/', views.favoritos_alto_valor_view, name='favoritos_alto_valor_view'),

    # Ejercicio 8: Medición de consultas y optimización N+1
    path('optimizacion/', views.optimizacion_nplus1_view, name='optimizacion_nplus1_view'),

    # Ejercicio 10: Transaccional en la investigación propia
    path('procesar-pedido/<int:pk>/', views.procesar_pedido_confirm, name='procesar_pedido_confirm'),

    # Ejercicio 11: Reporte de ventas con aggregate y annotate
    path('reporte-ventas/', views.reporte_ventas_view, name='reporte_ventas_view'),

    # Ejercicio 12: QuerySet personalizado en la investigación propia
    path('pedidos-pendientes/', views.pedidos_pendientes_view, name='pedidos_pendientes_list'),
    path('pedidos-pendientes/mayor-a/<str:umbral>/', views.pedidos_pendientes_view, name='pedidos_pendientes_mayor_a'),

    # Ejercicio 13: Medición y optimización N+1 en Pedidos
    path('optimizacion-pedidos/', views.optimizacion_nplus1_pedidos_view, name='optimizacion_nplus1_pedidos_view'),
]
