from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalogo.models import Categoria, Inventario, Marca, Producto, Proveedor
from clientes.models import Cliente, Direccion, MetodoPago
from .models import Cupon, DetallePedido, Envio, Pago, Pedido


class PantallasRelacionadasTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cliente = Cliente.objects.create(
            nombre='Ana', apellido='Pérez', email='ana@example.com', telefono='123456789'
        )
        cls.producto = Producto.objects.create(
            nombre='Cuaderno', descripcion='Rayado', precio='12.00',
            categoria=Categoria.objects.create(nombre='Útiles'),
            marca=Marca.objects.create(nombre='Marca A'),
            proveedor=Proveedor.objects.create(nombre='Proveedor A', telefono='123', email='p@example.com'),
        )
        cls.pedido = Pedido.objects.create(cliente=cls.cliente, total='24.00')
        DetallePedido.objects.create(
            pedido=cls.pedido, producto=cls.producto,
            cantidad=2, precio_unitario='12.00', subtotal='24.00',
        )

    def test_paginas_principales_y_formularios_con_herencia(self):
        for nombre in (
            'catalogo:inicio', 'catalogo:lista_productos', 'catalogo:lista_categorias',
            'catalogo:lista_marcas', 'catalogo:lista_proveedores', 'catalogo:lista_inventarios',
            'ventas:inicio', 'ventas:lista_pedidos', 'ventas:lista_detalles',
            'ventas:lista_pagos', 'ventas:lista_envios', 'ventas:lista_cupones',
            'catalogo:crear_producto', 'catalogo:crear_inventario',
            'ventas:crear_pedido', 'ventas:crear_detalle',
            'ventas:crear_pago', 'ventas:crear_envio',
        ):
            with self.subTest(ruta=nombre):
                respuesta = self.client.get(reverse(nombre))
                self.assertEqual(respuesta.status_code, 200)
                self.assertContains(respuesta, 'Tienda Online')

    def test_catalogo_y_pedido_con_relaciones_opcionales(self):
        respuesta = self.client.get(reverse('catalogo:lista_productos'))
        self.assertContains(respuesta, 'Sin inventario')
        self.assertContains(respuesta, 'Proveedor A')

        respuesta = self.client.get(reverse('ventas:lista_pedidos'))
        self.assertContains(respuesta, 'Ana Pérez')
        self.assertContains(respuesta, 'Cuaderno')
        self.assertContains(respuesta, 'Sin pago')
        self.assertContains(respuesta, 'Sin envío')

        Inventario.objects.create(producto=self.producto, cantidad=2, stock_minimo=5)
        metodo = MetodoPago.objects.create(tipo='Tarjeta', proveedor='Banco')
        direccion = Direccion.objects.create(
            cliente=self.cliente, calle='Calle 1', ciudad='Lima', codigo_postal='10000'
        )
        Pago.objects.create(pedido=self.pedido, metodo_pago=metodo, monto='24.00')
        Envio.objects.create(pedido=self.pedido, direccion=direccion, empresa_envio='Transporte')

        self.assertContains(self.client.get(reverse('catalogo:lista_productos')), 'Stock bajo')
        respuesta = self.client.get(reverse('ventas:lista_pedidos'))
        self.assertContains(respuesta, 'Pago: Pendiente')
        self.assertContains(respuesta, 'Envío: Pendiente')

    def test_admin_carga_listados_y_formulario_con_inlines(self):
        usuario = get_user_model().objects.create_superuser('admin_prueba', 'admin@example.com', 'clave123')
        self.client.force_login(usuario)
        for modelo in (Categoria, Marca, Proveedor, Producto, Inventario,
                       Pedido, DetallePedido, Pago, Envio, Cupon):
            self.assertIn(modelo, admin.site._registry)
            url = reverse(f'admin:{modelo._meta.app_label}_{modelo._meta.model_name}_changelist')
            self.assertEqual(self.client.get(url).status_code, 200, url)

        for modelo, objeto in ((Producto, self.producto), (Pedido, self.pedido)):
            url = reverse(f'admin:{modelo._meta.app_label}_{modelo._meta.model_name}_change', args=[objeto.pk])
            self.assertEqual(self.client.get(url).status_code, 200, url)
            url = reverse(f'admin:{modelo._meta.app_label}_{modelo._meta.model_name}_add')
            self.assertEqual(self.client.get(url).status_code, 200, url)
