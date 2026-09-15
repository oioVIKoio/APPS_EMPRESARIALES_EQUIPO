from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from catalogo.models import Categoria, Inventario, Marca, Producto, Proveedor
from clientes.models import Cliente, Direccion, Favorito, MetodoPago, PerfilCliente, Resena
from clientes.models import Carrito
from ventas.models import Cupon, DetallePedido, Envio, Pago, Pedido


class Command(BaseCommand):
    help = 'Crea datos de prueba relacionados para clientes, catalogo y ventas.'

    @transaction.atomic
    def handle(self, *args, **options):
        categoria, _ = Categoria.objects.get_or_create(
            nombre='Tecnologia',
            defaults={'descripcion': 'Productos tecnologicos de prueba'},
        )
        categoria_2, _ = Categoria.objects.get_or_create(
            nombre='Accesorios',
            defaults={'descripcion': 'Accesorios para equipos electronicos'},
        )

        marca, _ = Marca.objects.get_or_create(
            nombre='TechNova',
            defaults={'descripcion': 'Marca de tecnologia de prueba'},
        )
        marca_2, _ = Marca.objects.get_or_create(
            nombre='AulaDigital',
            defaults={'descripcion': 'Marca de accesorios de prueba'},
        )

        proveedor, _ = Proveedor.objects.get_or_create(
            email='ventas@distribuidora.test',
            defaults={
                'nombre': 'Distribuidora Central',
                'telefono': '999111222',
            },
        )
        proveedor_2, _ = Proveedor.objects.get_or_create(
            email='contacto@importaciones.test',
            defaults={
                'nombre': 'Importaciones Andinas',
                'telefono': '999333444',
            },
        )

        producto, _ = Producto.objects.get_or_create(
            nombre='Laptop Pro 14',
            defaults={
                'categoria': categoria,
                'marca': marca,
                'proveedor': proveedor,
                'descripcion': 'Laptop de prueba para el catalogo.',
                'precio': Decimal('2499.90'),
            },
        )
        producto_2, _ = Producto.objects.get_or_create(
            nombre='Mouse Inalambrico',
            defaults={
                'categoria': categoria_2,
                'marca': marca_2,
                'proveedor': proveedor_2,
                'descripcion': 'Mouse ergonomico de prueba.',
                'precio': Decimal('79.90'),
            },
        )
        Inventario.objects.get_or_create(
            producto=producto,
            defaults={'cantidad': 15, 'stock_minimo': 5},
        )
        Inventario.objects.get_or_create(
            producto=producto_2,
            defaults={'cantidad': 40, 'stock_minimo': 10},
        )

        cliente, _ = Cliente.objects.get_or_create(
            email='ana.prueba@example.com',
            defaults={
                'nombre': 'Ana',
                'apellido': 'Torres',
                'telefono': '987654321',
            },
        )
        cliente_2, _ = Cliente.objects.get_or_create(
            email='luis.prueba@example.com',
            defaults={
                'nombre': 'Luis',
                'apellido': 'Ramirez',
                'telefono': '986123456',
            },
        )

        MetodoPago.objects.get_or_create(
            tipo='Tarjeta',
            proveedor='Visa',
            defaults={'activo': True},
        )
        metodo_pago, _ = MetodoPago.objects.get_or_create(
            tipo='Yape',
            proveedor='Yape',
            defaults={'activo': True},
        )
        MetodoPago.objects.get_or_create(
            tipo='Transferencia',
            proveedor='BCP',
            defaults={'activo': True},
        )

        Carrito.objects.get_or_create(estado='Activo')
        Carrito.objects.get_or_create(estado='Comprado')

        direccion, _ = Direccion.objects.get_or_create(
            cliente=cliente,
            calle='Av. Las Flores 123',
            defaults={'ciudad': 'Lima', 'codigo_postal': '15001'},
        )
        Direccion.objects.get_or_create(
            cliente=cliente_2,
            calle='Jr. Los Olivos 456',
            defaults={'ciudad': 'Lima', 'codigo_postal': '15301'},
        )

        PerfilCliente.objects.get_or_create(
            cliente=cliente,
            defaults={
                'fecha_nacimiento': date(1998, 5, 12),
                'genero': 'Femenino',
                'recibir_newsletter': True,
                'preferencias': 'Tecnologia y ofertas especiales',
            },
        )
        PerfilCliente.objects.get_or_create(
            cliente=cliente_2,
            defaults={
                'fecha_nacimiento': date(1995, 9, 20),
                'genero': 'Masculino',
                'recibir_newsletter': False,
                'preferencias': 'Accesorios para computadoras',
            },
        )

        Favorito.objects.get_or_create(
            cliente=cliente,
            producto=producto,
            defaults={'notificar_oferta': True},
        )
        Favorito.objects.get_or_create(
            cliente=cliente_2,
            producto=producto_2,
            defaults={'notificar_oferta': False},
        )

        Resena.objects.get_or_create(
            cliente=cliente,
            comentario='Producto excelente y entrega rapida.',
            defaults={'calificacion': 5},
        )
        Resena.objects.get_or_create(
            cliente=cliente_2,
            comentario='Buen producto para el trabajo diario.',
            defaults={'calificacion': 4},
        )

        pedido, _ = Pedido.objects.get_or_create(
            cliente=cliente,
            estado='Confirmado',
            total=Decimal('2579.80'),
        )
        DetallePedido.objects.get_or_create(
            pedido=pedido,
            producto=producto,
            defaults={
                'cantidad': 1,
                'precio_unitario': Decimal('2499.90'),
                'subtotal': Decimal('2499.90'),
            },
        )
        DetallePedido.objects.get_or_create(
            pedido=pedido,
            producto=producto_2,
            defaults={
                'cantidad': 1,
                'precio_unitario': Decimal('79.90'),
                'subtotal': Decimal('79.90'),
            },
        )
        Pago.objects.get_or_create(
            pedido=pedido,
            defaults={
                'metodo_pago': metodo_pago,
                'monto': Decimal('2579.80'),
                'estado': 'Completado',
                'fecha_pago': timezone.now(),
            },
        )
        Envio.objects.get_or_create(
            pedido=pedido,
            defaults={
                'direccion': direccion,
                'empresa_envio': 'Olva Courier',
                'estado': 'En transito',
            },
        )

        Cupon.objects.get_or_create(
            codigo='BIENVENIDA10',
            defaults={
                'descripcion': 'Descuento de bienvenida',
                'descuento': Decimal('10.00'),
                'fecha_inicio': date.today(),
                'fecha_fin': date(date.today().year, 12, 31),
                'activo': True,
            },
        )

        self.stdout.write(self.style.SUCCESS(
            'Datos de prueba creados correctamente en clientes, catalogo y ventas.'
        ))
