from django.db import models


class Cliente(models.Model):
    """Modelo principal para gestionar la información de clientes"""
    id_cliente = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateTimeField(auto_now_add=True)

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
