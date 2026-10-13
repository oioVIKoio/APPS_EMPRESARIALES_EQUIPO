from decimal import Decimal, InvalidOperation

from rest_framework import filters, generics, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ventas.models import Cupon, DetallePedido, Pedido
from .models import Favorito, Resena
from .serializers import (
    CuponSerializer, DetallePedidoSerializer, FavoritoSerializer, PedidoSerializer, ResenaSerializer,
)


# Lab 08 - Ej. 4: vistas genéricas de Reseña
class ResenaListCreateView(generics.ListCreateAPIView):
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer


class ResenaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer


# Lab 08 - Ej. 5 y 8: ViewSet de Reseña con búsqueda y ordenamiento
class ResenaViewSet(viewsets.ModelViewSet):
    queryset = Resena.objects.order_by('id_resena')
    serializer_class = ResenaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['comentario', 'cliente__nombre', 'cliente__apellido']
    ordering_fields = ['calificacion', 'fecha']


# Lab 08 - Ej. 7 y 8: Favoritos de solo lectura, filtro ?estado= y acción propia
class FavoritoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FavoritoSerializer

    def get_queryset(self):
        queryset = Favorito.objects.select_related('cliente', 'producto__categoria')
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    @action(detail=False)
    def activos(self, request):
        queryset = self.get_queryset().favoritos_activos()
        min_puntos = request.query_params.get('min_puntos')
        if min_puntos:
            if not min_puntos.isdigit():
                raise ValidationError({'min_puntos': 'Debe ser un número entero.'})
            queryset = queryset.con_valor_mayor_a(int(min_puntos))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# Lab 08 - Ej. 11 y 13: Cupones con búsqueda y ordenamiento
class CuponViewSet(viewsets.ModelViewSet):
    queryset = Cupon.objects.order_by('id_cupon')
    serializer_class = CuponSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['codigo', 'descripcion']
    ordering_fields = ['descuento', 'fecha_fin']


# Lab 08 - Ej. 11: detalles de pedido (CRUD)
class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.select_related('producto').order_by('id_detalle')
    serializer_class = DetallePedidoSerializer


# Lab 08 - Ej. 12 y 13: Pedidos de solo lectura, filtro ?estado= y acción propia
class PedidoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PedidoSerializer

    def get_queryset(self):
        queryset = (
            Pedido.objects.select_related('cliente')
            .prefetch_related('detalles__producto')
            .order_by('id_pedido')
        )
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    @action(detail=False)
    def pendientes(self, request):
        queryset = self.get_queryset().pedidos_pendientes()
        total_min = request.query_params.get('total_min')
        if total_min:
            try:
                queryset = queryset.con_mayor_a(Decimal(total_min))
            except InvalidOperation:
                raise ValidationError({'total_min': 'Debe ser un número.'})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
