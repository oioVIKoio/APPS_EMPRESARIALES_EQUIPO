# Tienda Online

Proyecto desarrollado para el curso de **Desarrollo de Aplicaciones Empresariales**.

## Descripción

Sistema web de una tienda online desarrollado con **Django**, utilizando el patrón **MVT**, Django ORM y **SQLite** como base de datos.

El proyecto está dividido en tres aplicaciones:

* `clientes/` — Gestión de clientes.
* `catalogo/` — Gestión del catálogo de productos.
* `ventas/` — Gestión de pedidos y ventas.

## Modelo de datos

El proyecto utiliza relaciones entre modelos mediante Django ORM.

### Clientes

* `Cliente` se relaciona con `PerfilCliente` mediante una relación uno a uno (`OneToOneField`).
* `Cliente` se relaciona con `Direccion` y `Resena` mediante relaciones uno a muchos (`ForeignKey`).
* `Cliente` se relaciona con `Producto` mediante una relación muchos a muchos (`ManyToManyField`) utilizando `Favorito` como modelo intermedio.
* `Favorito` almacena información propia de la relación mediante `fecha_agregado` y `notificar_oferta`.

### Catálogo

* `Producto` se relaciona con `Categoria`, `Marca` y `Proveedor` mediante `ForeignKey`.
* `Inventario` se relaciona con `Producto` mediante `OneToOneField`.

### Ventas

* `Pedido` se relaciona con `Cliente`.
* `DetallePedido` relaciona los pedidos con sus productos.
* `Pago` y `Envio` se relacionan con `Pedido`.

## Tecnologías

* Python
* Django 5.2.13
* SQLite
* Django ORM
* HTML / Templates

## Equipo

* Diego — App `clientes`
* Victor — App `catalogo`
* Davila — App `ventas`

## Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/oioVIKoio/APPS_EMPRESARIALES_EQUIPO.git
cd APPS_EMPRESARIALES_EQUIPO