from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register('resenas', api_views.ResenaViewSet, basename='resena')
router.register('favoritos', api_views.FavoritoViewSet, basename='favorito')
router.register('cupones', api_views.CuponViewSet, basename='cupon')
router.register('detalles-pedido', api_views.DetallePedidoViewSet, basename='detalle-pedido')
router.register('pedidos', api_views.PedidoViewSet, basename='pedido')

urlpatterns = [
    # Ej. 4: vistas genéricas (se mantienen como referencia)
    path('genericas/resenas/', api_views.ResenaListCreateView.as_view(), name='resena_generica_list'),
    path('genericas/resenas/<int:pk>/', api_views.ResenaDetailView.as_view(), name='resena_generica_detail'),
    # Ej. 5: router
    path('', include(router.urls)),
]
