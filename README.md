# Tienda Online

Proyecto desarrollado para el curso de **Desarrollo de Aplicaciones Empresariales**.

## Descripción

Sistema web de una tienda online desarrollado con **Django**, utilizando el patrón **MVT**, Django ORM y **SQLite** como base de datos.

El proyecto está dividido en tres aplicaciones principales:

- `clientes/` — Gestión de clientes.
- `catalogo/` — Gestión del catálogo de productos.
- `ventas/` — Gestión de pedidos y ventas.

## Modelo de datos

El proyecto utiliza relaciones entre modelos mediante Django ORM.

### Clientes

- `Cliente` se relaciona con `PerfilCliente` mediante una relación uno a uno (`OneToOneField`).
- `Cliente` se relaciona con `Direccion` y `Resena` mediante relaciones uno a muchos (`ForeignKey`).
- `Cliente` se relaciona con `Producto` mediante una relación muchos a muchos (`ManyToManyField`), utilizando `Favorito` como modelo intermedio.
- `Favorito` almacena información propia de la relación mediante `fecha_agregado` y `notificar_oferta`.

### Catálogo

- `Producto` se relaciona con `Categoria`, `Marca` y `Proveedor` mediante `ForeignKey`.
- `Inventario` se relaciona con `Producto` mediante `OneToOneField`.

### Ventas

- `Pedido` se relaciona con `Cliente`.
- `DetallePedido` relaciona los pedidos con sus productos.
- `Pago` y `Envio` se relacionan con `Pedido`.

## Tecnologías

- Python
- Django 5.2.13
- SQLite
- Django ORM
- HTML
- Django Templates
- Bootstrap

## Administración con Django Admin

Django Admin se utiliza como interfaz de administración interna para gestionar los datos y relaciones principales del sistema.

### Clientes

En el módulo `clientes` se administran las siguientes entidades:

- Cliente
- MetodoPago
- Carrito
- Direccion
- Resena
- PerfilCliente
- Favorito

Se utilizaron clases `ModelAdmin` para mejorar la visualización y consulta de los registros:

- **Cliente:** utiliza `list_display`, `search_fields` y `list_filter`.
- **Direccion:** utiliza `list_display` y `search_fields`.
- **Resena:** utiliza `list_display`, `search_fields` y `list_filter`.

También se utilizan Inlines para gestionar relaciones directamente desde el formulario de un cliente:

- **`PerfilClienteInline` (`StackedInline`):** permite administrar el perfil asociado mediante su relación `OneToOneField`.
- **`FavoritoInline` (`TabularInline`):** permite administrar la relación muchos a muchos entre Cliente y Producto mediante el modelo intermedio `Favorito`.

### Catálogo

Se configuraron administradores personalizados para:

- Categoria
- Marca
- Proveedor
- Producto
- Inventario

La administración de productos incorpora herramientas de búsqueda, filtros y visualización de información relacionada.

Además, `Inventario` puede administrarse directamente desde `Producto` mediante un Inline, aprovechando la relación `OneToOneField` existente entre ambos modelos.

### Ventas

Se personalizó la administración de:

- Pedido
- DetallePedido
- Pago
- Envio
- Cupon

`Pedido` funciona como una de las entidades principales del flujo de ventas y permite gestionar información relacionada mediante Inlines:

- **`DetallePedidoInline`:** administra los productos y cantidades asociados al pedido.
- **`PagoInline`:** permite administrar el pago relacionado.
- **`EnvioInline`:** permite administrar la información de envío.

De esta manera, Django Admin permite consultar y gestionar las principales relaciones del sistema desde interfaces centralizadas.

## Organización de Templates

Los módulos `catalogo` y `ventas` utilizan herencia de templates para reducir la duplicación de código y mantener una interfaz consistente.

La estructura reutiliza templates base y componentes CRUD para las operaciones de:

- Listado.
- Creación y edición.
- Eliminación.

Los templates específicos de cada entidad extienden estas estructuras y definen únicamente el contenido necesario mediante bloques de Django Templates.

De esta forma se aplica el principio **DRY (Don't Repeat Yourself)** y se mantiene separada la lógica correspondiente a cada aplicación.

## Integración entre módulos

Las aplicaciones mantienen responsabilidades separadas, pero se comunican mediante las relaciones definidas con Django ORM.

El flujo principal del sistema puede representarse de forma simplificada como:

```text
Cliente
   │
   ▼
Pedido
   │
   ├──► Pago
   ├──► Envio
   │
   ▼
DetallePedido
   │
   ▼
Producto
   │
   ├──► Categoria
   ├──► Marca
   ├──► Proveedor
   └──► Inventario
```

A partir de estas relaciones:

- `ventas` utiliza los clientes registrados en `clientes`.
- `DetallePedido` conecta los pedidos con los productos de `catalogo`.
- Cada producto puede relacionarse con su inventario.
- Cada pedido puede relacionarse con sus detalles, pago y envío.

Esta organización permite conectar los módulos sin duplicar modelos ni mezclar sus responsabilidades.

## Laboratorio N° 07 — Django ORM Avanzado

Este proyecto implementa **14 ejercicios** de Django ORM avanzado, organizados en dos partes:

### PARTE 1 — Consultas avanzadas sobre la aplicación base

| Ejercicio | Descripción |
|-----------|-------------|
| 1 | Entidad principal, 3 relaciones, modelo intermedio N:M |
| 2 | Carga de datos de prueba (5 clientes, 3× categorías/marcas/proveedores, 8 productos, 8 favoritos) |
| 3 | Operación transaccional con `transaction.atomic()` y `F()` + patrón PRG |
| 4 | Total global con `aggregate()` (Sum, Count) |
| 5 | Valores por objeto con `annotate()` agrupados por estado y cliente |
| 6 | Página de reporte con filtros de plantilla (`floatformat`) |
| 7 | QuerySet personalizado (`as_manager()`) con métodos encadenables |
| 8 | Medición y optimización N+1 con `select_related()` y `prefetch_related()` |

### PARTE 2 — Consultas avanzadas sobre la investigación propia (7 entidades adicionales)

| Ejercicio | Descripción |
|-----------|-------------|
| 9 | Tabla de equivalencias de 14 entidades del e-commerce |
| 10 | Operación transaccional en investigación propia (procesar pago de pedido) |
| 11 | Reporte de ventas con `aggregate()` y `annotate()` (global, por estado, por cliente) |
| 12 | QuerySet personalizado para `Pedido` (pendientes, mayor a umbral) |
| 13 | Medición y optimización N+1 en Pedidos con select_related/prefetch_related |
| 14 | Actualización de requirements.txt y README.md |

### URLs implementadas

| URL | Vista | Ejercicio |
|-----|-------|-----------|
| `/clientes/` | `cliente_list` | CRUD base |
| `/reporte/` | `reporte_view` | Ej. 6 |
| `/favoritos/activos/` | `favoritos_activos_view` | Ej. 7 |
| `/optimizacion/` | `optimizacion_nplus1_view` | Ej. 8 |
| `/procesar-pedido/<pk>/` | `procesar_pedido_confirm` | Ej. 10 |
| `/reporte-ventas/` | `reporte_ventas_view` | Ej. 11 |
| `/pedidos-pendientes/` | `pedidos_pendientes_view` | Ej. 12 |
| `/optimizacion-pedidos/` | `optimizacion_nplus1_pedidos_view` | Ej. 13 |

## Autores

- **Santamaria Fabian, Victor Manuel**

- **Panez Rondinel, Diego Daniel**

## Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/oioVIKoio/APPS_EMPRESARIALES_EQUIPO.git
cd APPS_EMPRESARIALES_EQUIPO
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

En Windows:

```powershell
.venv\Scripts\activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar las migraciones

```bash
python manage.py migrate
```

### 5. Crear un superusuario

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor

```bash
python manage.py runserver
```

La aplicación estará disponible en:

```text
http://127.0.0.1:8000/
```

El panel administrativo estará disponible en:

```text
http://127.0.0.1:8000/admin/
```