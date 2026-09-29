from django.db import models
from django.db.models import Count, Sum


class Cliente(models.Model):
    """Modelo principal para gestionar la información de clientes"""
    id_cliente = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    productos_favoritos = models.ManyToManyField(
        'catalogo.Producto',
        through='Favorito',
        related_name='clientes_que_lo_favoritearon'
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.email})"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class MetodoPago(models.Model):
    """Modelo para gestionar los métodos de pago disponibles"""
    id_pago = models.BigAutoField(primary_key=True)
    tipo = models.CharField(max_length=50)
    proveedor = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tipo} - {self.proveedor}"

    class Meta:
        verbose_name = "Método de Pago"
        verbose_name_plural = "Métodos de Pago"


class Carrito(models.Model):
    """Modelo para gestionar los carritos de compra"""
    id_carrito = models.BigAutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='Activo')

    def __str__(self):
        return f"Carrito {self.id_carrito} - {self.estado}"

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"


class Direccion(models.Model):
    """Modelo para gestionar direcciones asociadas a clientes"""
    id_direccion = models.BigAutoField(primary_key=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='direcciones'
    )
    calle = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.calle}, {self.ciudad} ({self.codigo_postal}) - {self.cliente.nombre}"

    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"


class Resena(models.Model):
    """Modelo para gestionar reseñas y valoraciones de clientes"""
    id_resena = models.BigAutoField(primary_key=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='resenas'
    )
    comentario = models.TextField()
    calificacion = models.IntegerField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Reseña de {self.cliente.nombre} - Calificación: {self.calificacion}/5"

    class Meta:
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"

class PerfilCliente(models.Model):
    cliente = models.OneToOneField(
        Cliente,
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=20, blank=True)
    recibir_newsletter = models.BooleanField(default=True)
    preferencias = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.cliente.nombre}"

class Favorito(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('oferta', 'En Oferta'),
        ('comprado', 'Comprado'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='favoritos'
    )
    producto = models.ForeignKey(
        'catalogo.Producto',
        on_delete=models.CASCADE,
        related_name='favorito_de'
    )
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    notificar_oferta = models.BooleanField(default=False)

    # Campos para ORM Avanzado (Laboratorio N° 07)
    descuento_puntos = models.PositiveIntegerField(default=0, help_text="Puntos a descontar del carrito")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    prioridad = models.PositiveIntegerField(default=1, help_text="Prioridad del favorito (1=más importante)")

    class Meta:
        unique_together = ('cliente', 'producto')
        ordering = ['-prioridad', '-fecha_agregado']

    def __str__(self):
        return f"{self.cliente.nombre} ♥ {self.producto.nombre}"

    # ═══════════════════════════════════════════════════════════
    # Ejercicio 7: QuerySet personalizado con as_manager()
    # ═══════════════════════════════════════════════════════════

    class FavoriteManager(models.Manager):
        """Manager personalizado que expone métodos de regla de negocio."""

        def get_queryset(self):
            return FavoritoCustomQuerySet(self.model, using=self._db)

        def favoritos_activos(self):
            """Retorna solo los favoritos con estado 'activo'."""
            return self.get_queryset().favoritos_activos()

        def con_valor_mayor_a(self, puntos):
            """Retorna favoritos donde descuento_puntos > el valor dado."""
            return self.get_queryset().con_valor_mayor_a(puntos)

        def resumen_por_cliente(self):
            """Retorna un QuerySet con conteo por cliente (encadenable)."""
            return self.get_queryset().resumen_por_cliente()

    objects = FavoriteManager()


# ═══════════════════════════════════════════════════════════
# QuerySet personalizado para Ejercicio 7 (as_manager)
# ═══════════════════════════════════════════════════════════

class FavoritoCustomQuerySet(models.QuerySet):
    """QuerySet personalizado para Favorito con métodos de regla de negocio."""

    def favoritos_activos(self):
        """Retorna solo los favoritos con estado 'activo'."""
        return self.filter(estado='activo')

    def con_valor_mayor_a(self, puntos):
        """Retorna favoritos donde descuento_puntos > el valor dado."""
        return self.filter(descuento_puntos__gt=puntos)

    def resumen_por_cliente(self):
        """Retorna un QuerySet con conteo por cliente (encadenable)."""
        return (
            self.values('cliente__nombre')
            .annotate(
                total_favoritos=Count('id'),
                total_descuento=Sum('descuento_puntos')
            )
            .order_by('-total_descuento')
        )


# ═══════════════════════════════════════════════════════════
# Ejercicio 9: Tabla de equivalencias (Documentación de modelos)
# ═══════════════════════════════════════════════════════════

# ┌─────────────────────────┬──────────────────────────────────────┬──────────┬──────────────────┬────────────────────────────────────┐
# │ ENTIDAD / MODELO        │ CAMPOS                               │ TIPO REL │ RELATIONSHIP       │ RELATED NAME(S)                   │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ Cliente                 │ id_cliente, nombre, apellido, email, │ 1:N      │ Cliente → Direccion │ direcciones                      │
# │                         │ telefono, fecha_registro             │          │ Cliente → Resena   │ resenas                          │
# │                         │                                      │          │ Cliente → Favorito │ favoritos                        │
# │                         │                                      │ 1:1      │ Cliente → Perfil    │ perfil                           │
# │                         │                                      │ N:M      │ Cliente ↔ Producto │ clientes_que_lo_favoritearon     │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ MetodoPago              │ id_pago, tipo, proveedor, activo     │ 1:N      │ MetodoPago → Pago  │ pagos                            │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ Carrito                 │ id_carrito, fecha_creacion, estado   │ 1:0..1   │ Carrito → Cliente  │ (sin FK directa — se usa por     │
# │                         │                                      │          │                    │ sesión o relación manual)         │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ Direccion               │ id_direccion, calle, ciudad,         │ N:1      │ Direccion → Cliente │ related_name='direcciones'       │
# │                         │ codigo_postal, cliente (FK)          │          │                    │                                    │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ Resena                  │ id_resena, cliente (FK),             │ N:1      │ Resena → Cliente   │ related_name='resenas'           │
# │                         │ comentario, calificacion, fecha      │          │                    │                                    │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ PerfilCliente           │ cliente (OneToOne), fecha_nacimiento│ 1:1      │ Cliente → Perfil    │ related_name='perfil'            │
# │                         │, genero, recibir_newsletter,         │          │ Perfil → Cliente   │ (backwards via perfil)           │
# │                         │ preferencias                         │          │                    │                                    │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ Favorito                │ id, cliente (FK), producto (FK),     │ N:1      │ Favorito → Cliente │ related_name='favoritos'         │
# │                         │ fecha_agregado, notificar_oferta,    │ N:1      │ Favorito → Producto │ related_name='favorito_de'       │
# │                         │ descuento_puntos, estado, prioridad  │          │ (through table)    │ (N:M bridge between Cliente y    │
# │                         │                                      │          │                    │ Producto)                        │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ Categoria (catalogo)    │ id_categoria, nombre, descripcion    │ 1:N      │ Categoria → Producto │ productos (auto)                 │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ Marca (catalogo)        │ id_marca, nombre, descripcion        │ 1:N      │ Marca → Producto   │ productos (auto)                 │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ Proveedor (catalogo)    │ id_proveedor, nombre, telefono,      │ 1:N      │ Proveedor → Producto │ productos (auto)                │
# │                         │ email                                │          │                    │                                    │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ Producto (catalogo)     │ id_producto, nombre, precio,         │ N:1      │ Producto → Categoria  │ related_name='productos'        │
# │                         │ descripcion, categoria, marca,       │ N:1      │ Producto → Marca      │ related_name='productos'        │
# │                         │ proveedor, stock, fecha_creacion     │ N:1      │ Producto → Proveedor  │ related_name='productos'        │
# │                         │                                      │ 1:1      │ Producto → Inventario │ inventario (auto)               │
# │                         │                                      │ N:M      │ Producto ↔ Cliente   │ related_name='clientes_que_lo_   │
# │                         │                                      │          │ (via Favorito)      │ favoritearon                     │
# │                         │                                      │ 1:N      │ Producto → DetallePedido │ related_name='detalles_pedido' │
# │                         │                                      │          │                    │                                    │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ Inventario (catalogo)   │ id_inventario, producto (OneToOne),  │ 1:1      │ Inventario → Producto │ related_name='inventario'        │
# │                         │ cantidad, stock_minimo               │          │                    │                                    │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ Pedido (ventas)         │ id_pedido, cliente (FK),             │ N:1      │ Pedido → Cliente    │ related_name='pedidos'           │
# │                         │ fecha_pedido, estado, total          │          │                    │                                    │
# │                         │                                      │ N:M      │ Pedido ↔ Producto   │ related_name='pedidos' (via      │
# │                         │                                      │          │ (via DetallePedido)  │ DetallePedido)                    │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ DetallePedido (ventas)  │ id_detalle, pedido (FK),             │ N:1      │ DetallePedido → Pedido  │ related_name='detalles'         │
# │                         │ producto (FK), cantidad,             │ N:1      │ DetallePedido → Producto│ related_name='detalles_pedido'  │
# │                         │ precio_unitario, subtotal            │          │                    │                                    │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ Pago (ventas)           │ id_pago, pedido (OneToOne),          │ 1:1      │ Pago → Pedido       │ related_name='pago'              │
# │                         │ metodo_pago (FK), monto, estado,     │ N:1      │ Pago → MetodoPago   │ related_name='pagos'             │
# │                         │ fecha_pago                           │          │                    │                                    │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ Envio (ventas)          │ id_envio, pedido (OneToOne),         │ 1:1      │ Envio → Pedido      │ related_name='envio'             │
# │                         │ direccion (FK), empresa_envio,       │ N:1      │ Envio → Direccion   │ related_name='envios'            │
# │                         │ estado, fecha_envio, fecha_entrega   │          │                    │                                    │
# ├─────────────────────────┼──────────────────────────────────────┼──────────┼────────────────────┼────────────────────────────────────┤
# │ Cupon (ventas)          │ id_cupon, codigo, descripcion,       │ —        │ (sin relaciones     │ (sin relaciones FK)              │
# │                         │ descuento, fecha_inicio, fecha_fin,  │          │  con otros modelos) │                                    │
# │                         │ activo                               │          │                    │                                    │
# └─────────────────────────┴──────────────────────────────────────┴──────────┴────────────────────┴────────────────────────────────────┘
