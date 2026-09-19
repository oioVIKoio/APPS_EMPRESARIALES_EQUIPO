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
* Victor — App `catalogo y ventas `

## Administración con Django Admin

Durante la Semana 5 se configuró y personalizó Django Admin para facilitar
la gestión de los datos del sistema.

### Modelos administrados

En el módulo `clientes` se registraron las siguientes entidades:

- Cliente
- MetodoPago
- Carrito
- Direccion
- Resena
- PerfilCliente
- Favorito

### Personalización de ModelAdmin

Se personalizaron distintas entidades utilizando `ModelAdmin`:

- **Cliente:** utiliza `list_display` para mostrar sus datos principales,
  `search_fields` para realizar búsquedas por nombre, apellido y correo,
  y `list_filter` para filtrar por fecha de registro.
- **Direccion:** utiliza `list_display` para mostrar los datos principales
  de la dirección y `search_fields` para realizar búsquedas.
- **Resena:** utiliza `list_display`, `search_fields` y `list_filter`
  para facilitar la administración de las reseñas.

### Gestión de relaciones mediante Inlines

Se utilizaron Inlines para administrar relaciones directamente desde
el formulario de Cliente:

- **PerfilClienteInline (`StackedInline`):** permite administrar el perfil
  relacionado mediante `OneToOneField` desde el mismo formulario del cliente.
- **FavoritoInline (`TabularInline`):** permite administrar la relación
  muchos a muchos entre Cliente y Producto mediante el modelo intermedio
  `Favorito`, incluyendo atributos como `fecha_agregado` y
  `notificar_oferta`.

Esta configuración permite realizar operaciones CRUD desde Django Admin
y gestionar las relaciones entre las entidades de forma centralizada.

## Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/oioVIKoio/APPS_EMPRESARIALES_EQUIPO.git
cd APPS_EMPRESARIALES_EQUIPO