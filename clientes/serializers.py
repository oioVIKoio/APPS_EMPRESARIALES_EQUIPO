from rest_framework import serializers

from catalogo.models import Producto
from ventas.models import Cupon, DetallePedido, Pedido
from .models import Cliente, Favorito, Resena


# Lab 08 - Ej. 2 y 3: serializer de Reseña con validación
class ResenaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resena
        fields = ['id_resena', 'cliente', 'comentario', 'calificacion', 'fecha']

    def validate_calificacion(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('La calificación debe estar entre 1 y 5.')
        return value


# Lab 08 - Ej. 7: Favorito con cliente y producto anidados (solo lectura)
class ClienteResumenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = ['id_cliente', 'nombre', 'apellido', 'email']


class ProductoResumenSerializer(serializers.ModelSerializer):
    categoria = serializers.CharField(source='categoria.nombre')

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'categoria']


class FavoritoSerializer(serializers.ModelSerializer):
    cliente = ClienteResumenSerializer()
    producto = ProductoResumenSerializer()

    class Meta:
        model = Favorito
        fields = ['id', 'cliente', 'producto', 'estado', 'descuento_puntos', 'prioridad', 'fecha_agregado']


# Lab 08 - Ej. 10: serializers de la investigación propia (ventas)
class CuponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cupon
        fields = ['id_cupon', 'codigo', 'descripcion', 'descuento', 'fecha_inicio', 'fecha_fin', 'activo']

    def validate_descuento(self, value):
        if value <= 0 or value > 100:
            raise serializers.ValidationError('El descuento debe ser mayor que 0 y como máximo 100.')
        return value

    def validate(self, data):
        inicio = data.get('fecha_inicio', getattr(self.instance, 'fecha_inicio', None))
        fin = data.get('fecha_fin', getattr(self.instance, 'fecha_fin', None))
        if inicio and fin and fin < inicio:
            raise serializers.ValidationError({'fecha_fin': 'La fecha de fin no puede ser anterior a la de inicio.'})
        return data


class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)

    class Meta:
        model = DetallePedido
        fields = ['id_detalle', 'pedido', 'producto', 'producto_nombre', 'cantidad', 'precio_unitario', 'subtotal']
        read_only_fields = ['subtotal']

    def validate_cantidad(self, value):
        if value < 1:
            raise serializers.ValidationError('La cantidad debe ser al menos 1.')
        return value

    def validate(self, data):
        cantidad = data.get('cantidad', getattr(self.instance, 'cantidad', None))
        precio = data.get('precio_unitario', getattr(self.instance, 'precio_unitario', None))
        data['subtotal'] = cantidad * precio
        return data


# Lab 08 - Ej. 12: Pedido con cliente y detalles anidados (solo lectura)
class PedidoSerializer(serializers.ModelSerializer):
    cliente = ClienteResumenSerializer()
    detalles = DetallePedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = ['id_pedido', 'cliente', 'fecha_pedido', 'estado', 'total', 'detalles']
