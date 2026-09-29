from django.db import models


# ═══════════════════════════════════════════════════════════
# Ejercicio 12: QuerySet personalizado para Pedido
# ═══════════════════════════════════════════════════════════

class PedidoCustomQuerySet(models.QuerySet):
    """QuerySet personalizado para Pedido con métodos de regla de negocio."""

    def pedidos_pendientes(self):
        """Filtra y retorna solo los pedidos con estado='Pendiente'."""
        return self.filter(estado='Pendiente')

    def con_mayor_a(self, monto):
        """Filtra y retorna pedidos con total > monto."""
        return self.filter(total__gt=monto)


class PedidoManager(models.Manager):
    """Manager personalizado que expone métodos de regla de negocio para Pedido."""

    def get_queryset(self):
        return PedidoCustomQuerySet(self.model, using=self._db)

    def pedidos_pendientes(self):
        """Retorna solo los pedidos con estado 'Pendiente'."""
        return self.get_queryset().pedidos_pendientes()

    def con_mayor_a(self, monto):
        """Retorna pedidos con total > monto."""
        return self.get_queryset().con_mayor_a(monto)


class Pedido(models.Model):
    id_pedido = models.BigAutoField(primary_key=True)

    # Ejercicio 12: Custom manager para QuerySet personalizado
    objects = PedidoManager()

    cliente = models.ForeignKey(
        'clientes.Cliente',
        on_delete=models.CASCADE,
        related_name='pedidos'
    )

    productos = models.ManyToManyField(
        'catalogo.Producto',
        through='DetallePedido',
        related_name='pedidos'
    )

    fecha_pedido = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(
        max_length=30,
        default='Pendiente'
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Pedido {self.id_pedido} - {self.cliente}"


class DetallePedido(models.Model):
    id_detalle = models.BigAutoField(primary_key=True)

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='detalles'
    )

    producto = models.ForeignKey(
        'catalogo.Producto',
        on_delete=models.CASCADE,
        related_name='detalles_pedido'
    )

    cantidad = models.PositiveIntegerField(default=1)

    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"Detalle {self.id_detalle} - Pedido {self.pedido.id_pedido}"


class Pago(models.Model):
    id_pago = models.BigAutoField(primary_key=True)

    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name='pago'
    )

    metodo_pago = models.ForeignKey(
        'clientes.MetodoPago',
        on_delete=models.PROTECT,
        related_name='pagos'
    )

    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    estado = models.CharField(
        max_length=30,
        default='Pendiente'
    )

    fecha_pago = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Pago {self.id_pago} - Pedido {self.pedido.id_pedido}"


class Envio(models.Model):
    id_envio = models.BigAutoField(primary_key=True)

    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name='envio'
    )

    direccion = models.ForeignKey(
        'clientes.Direccion',
        on_delete=models.PROTECT,
        related_name='envios'
    )

    empresa_envio = models.CharField(
        max_length=100
    )

    estado = models.CharField(
        max_length=30,
        default='Pendiente'
    )

    fecha_envio = models.DateTimeField(
        null=True,
        blank=True
    )

    fecha_entrega = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Envío {self.id_envio} - Pedido {self.pedido.id_pedido}"


class Cupon(models.Model):
    id_cupon = models.BigAutoField(primary_key=True)

    codigo = models.CharField(
        max_length=50,
        unique=True
    )

    descripcion = models.CharField(
        max_length=200,
        blank=True
    )

    descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    fecha_inicio = models.DateField()

    fecha_fin = models.DateField()

    activo = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.codigo