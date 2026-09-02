from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),
    
    path('marcas/', views.lista_marcas, name='lista_marcas'),
    path('marcas/crear/', views.crear_marca, name='crear_marca'),
    path('marcas/editar/<int:id>/', views.editar_marca, name='editar_marca'),
    path('marcas/eliminar/<int:id>/', views.eliminar_marca, name='eliminar_marca'),
    
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('proveedores/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    
    path('inventario/', views.lista_inventarios, name='lista_inventarios'),
    path('inventario/crear/', views.crear_inventario, name='crear_inventario'),
    path('inventario/editar/<int:id>/', views.editar_inventario, name='editar_inventario'),
    path('inventario/eliminar/<int:id>/', views.eliminar_inventario, name='eliminar_inventario'),
]