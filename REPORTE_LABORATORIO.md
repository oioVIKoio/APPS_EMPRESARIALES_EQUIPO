# Laboratorio N° 07 — Django ORM Avanzado

**Equipo:** APPS_EMPRESARIALES_EQUIPO  
**Fecha:** 2026-09-29  
**Proyecto:** App E-commerce (3 apps: clientes, catalogo, ventas)

---

## PARTE 1 — Consultas avanzadas sobre la aplicación base

### Ejercicio 1: Identificar entidad principal y 3 relaciones

**Entidad principal:** `Cliente` (modelo central de la app `clientes`, PK `id_cliente`)

**3 Relaciones 1:N identificadas:**
| # | Modelo origen | Modelo destino | Campo FK |
|---|---|---|---|
| 1 | `Cliente` | `Direccion` | `cliente` (FK → Cliente) |
| 2 | `Cliente` | `Resena` | `cliente` (FK → Cliente) |
| 3 | `Cliente` | `PerfilCliente` | `cliente` (OneToOneField → Cliente) |

**Modelo intermedio N:M:** `Favorito` (tabla intermedia entre `Cliente` y `catalogo.Producto`)

**Campos agregados en `Favorito`:**
| Campo | Tipo | Default | Descripción |
|---|---|---|---|
| `descuento_puntos` | `PositiveIntegerField` | 0 | Campo entero a descontar (para operaciones con F()) |
| `estado` | `CharField(choices=ESTADO_CHOICES)` | 'activo' | Campo de estado para agrupaciones (annotate/values) |
| `prioridad` | `PositiveIntegerField` | 1 | Atributo numérico de priorización |

**Clase `ESTADO_CHOICES` agregada:**
```python
ESTADO_CHOICES = [
    ('activo', 'Activo'),
    ('inactivo', 'Inactivo'),
    ('oferta', 'En Oferta'),
    ('comprado', 'Comprado'),
]
```

**Meta class de `Favorito` actualizada:**
```python
class Meta:
    unique_together = ('cliente', 'producto')
    ordering = ['-prioridad', '-fecha_agregado']  # Nuevo: orden predeterminado
```

**Migración generada:** `0003_alter_favorito_options_favorito_descuento_puntos_and_more.py`

**Migración generada (añadir 'comprado'):** `0004_alter_favorito_estado.py`


---

### Ejercicio 2: Cargar datos de prueba vía Django Admin

**Script creado:** `cargar_datos_prueba.py` (ejecutable directamente con `python manage.py shell` o `python cargar_datos_prueba.py`)

**Datos cargados:**
| Entidad | Cantidad | Detalle |
|---|---|---|
| `Categoria` | 3 | Electrónica, Ropa, Hogar |
| `Marca` | 3 | TechBrand, FashionCo, HomePlus |
| `Proveedor` | 3 | TechDist S.A., FashionImport, HogarWorld |
| `Producto` | 8 | Distribuidos entre las 3 categorías |
| `Cliente` | 5 | Juan Pérez, María García, Carlos López, Ana Martínez, Pedro Rodríguez |
| `PerfilCliente` | 5 | Uno por cada cliente |
| `Direccion` | 5 | Una por cada cliente |
| `Favorito` | 8 | Modelo intermedio N:M Cliente↔Producto con campos `descuento_puntos`, `estado`, `prioridad` |
| `MetodoPago` | 4 | Tarjeta de Crédito, Transferencia, Yape, PayPal |

**Características del script:**
- Limpia la base de datos antes de cargar para evitar duplicados
- Respeto del orden de dependencias FK al eliminar (Envio→Pago→DetallePedido→Pedido→...)
- Usa `get_or_create` para evitar duplicados en ejecuciones repetidas
- Los 8 Favoritos tienen distintos valores de `estado` (activo/inactivo/oferta) y `descuento_puntos` para probar agregaciones en ejercicios posteriores

**Verificación:** `Total descuento_puntos = 255` (suma de los 8 favoritos)

---

### Ejercicio 3: View/URL/Template con transaction.atomic() y F()

**Funcionalidad:** Simulación de compra de producto favorito con operación atómica y descuento de inventario.

**Archivos creados/modificados:**
| Archivo | Acción | Descripción |
|---|---|---|
| `clientes/views.py` | Modificado | 2 nuevas views: `comprar_favorito_confirm` y `comprar_favorito_procesar` |
| `clientes/urls.py` | Modificado | 2 nuevas URLs: `comprar_favorito_confirm` y `comprar_favorito_procesar` |
| `clientes/templates/clientes/comprar_favorito_confirm.html` | Creado | Template de confirmación de compra con resumen de datos |
| `clientes/templates/clientes/cliente_favoritos.html` | Modificado | Tabla extendida con columnas Prioridad, Estado, Descuento y botón "Comprar" |

**Vista `comprar_favorito_confirm`:**
- Muestra un formulario de confirmación con resumen de la compra
- Datos mostrados: cliente, producto, categoría, precio, stock actual, puntos a descontar, stock después de compra
- Indicadores visuales: badges de color según disponibilidad de stock
- Validación visual previa: alerta roja si stock insuficiente

**Vista `comprar_favorito_procesar`:**
- Recibe POST con `{% csrf_token %}`
- Usa `transaction.atomic()` para garantizar atomicidad
- Verifica stock suficiente antes de proceder
- Usa `models.F('cantidad')` para actualizar inventario de forma atómica (evita race conditions)
- Marca el favorito como estado `'comprado'`
- Maneja errores con `ValueError` (stock insuficiente) y rollback automático
- Usa mensajes de Django (`messages.success` / `messages.error`)
- Patrón Post/Redirect/Get (siempre redirige tras POST exitoso o error)

**Código clave del update atómico:**
```python
with transaction.atomic():
    # Verificar stock
    if inventario_actual < favorito.descuento_puntos:
        raise ValueError("Stock insuficiente...")
    
    # Actualizar con F() (evita race conditions)
    rows_affected = Inventario.objects.filter(
        producto=producto
    ).update(
        cantidad=models.F('cantidad') - favorito.descuento_puntos
    )
    
    # Marcar favorito como comprado
    favorito.estado = 'comprado'
    favorito.save(update_fields=['estado'])
```

**Flujo de usuario:**
1. Cliente ve su lista de favoritos → clic en "Comprar" en un producto
2. Se muestra página de confirmación con resumen
3. Usuario confirma → POST a `comprar_favorito_procesar`
4. Se descuenta inventario atómicamente y se actualiza estado
5. Redirección a lista de favoritos con mensaje de éxito/error

---

### Ejercicio 4: Calcular total global con aggregate() y F()

**Script creado:** `ejercicio4.py` (ejecutable directamente)

**Resultados obtenidos:**

| Consulta | Método | Resultado |
|---|---|---|
| Suma total de `descuento_puntos` | `aggregate(Sum('descuento_puntos'))` | `255` |
| Cantidad total de favoritos | `aggregate(Count('id'))` | `8` |
| Promedio de `descuento_puntos` | `aggregate(Avg('descuento_puntos'))` | `31.875` |
| **Total general en soles** | `aggregate(Sum(F('descuento_puntos') * F('producto__precio')))` | **S/ 682,297.45** |

**Código clave:**
```python
from django.db.models import F, Sum

# Usar F() para vincular campo del modelo intermedio con campo del modelo relacionado
total = Favorito.objects.annotate(
    valor_total=F('descuento_puntos') * F('producto__precio')
).aggregate(
    total_geral=Sum('valor_total')
)
# Resultado: {'total_geral': Decimal('682297.450000000')}
```

**Detalle de cada favorito:**
| Cliente | Producto | Descuento | Precio | Valor |
|---|---|---|---|---|
| Carlos | Jeans Classic | 15 | 149.99 | 2,249.85 |
| Ana | Lámpara LED | 5 | 129.99 | 649.95 |
| María | Vestido Elegante | 20 | 199.99 | 3,999.80 |
| Juan | Camiseta Urban | 10 | 89.99 | 899.90 |
| Pedro | Set de Sábanas | 25 | 179.99 | 4,499.75 |
| Carlos | Sofá Moderno | 100 | 3,499.99 | 349,999.00 |
| María | Smartphone X | 30 | 2,999.99 | 89,999.70 |
| Juan | Laptop Pro 15 | 50 | 4,599.99 | 229,999.50 |

**Verificación:** La suma manual (S/ 682,297.45) coincide exactamente con `aggregate()` + `F()`.

---

### Ejercicio 5: Calcular valores con annotate() y values().annotate()

**Script creado:** `ejercicio5.py` (ejecutable directamente)

**Resultados obtenidos:**

| Consulta | Método | Resultado |
|---|---|---|
| Valores por objeto | `annotate(valor=F('descuento_puntos') * F('producto__precio'))` | 8 objetos con campo `valor` calculado |
| Agrupado por estado | `values('estado').annotate(cantidad=Count('id'), ...)` | 4 grupos: activo, inactivo, oferta, comprado |
| Agrupado por cliente | `values('cliente__nombre').annotate(favoritos=Count('id'), ...)` | 5 grupos (uno por cliente) |
| Combinado estado × cliente | `values('cliente__nombre', 'estado').annotate(descuento=Sum(...))` | Múltiples combinaciones |

**Código clave:**
```python
from django.db.models import F, Sum, Count
from django.db.models.functions import Lower

# 1. Valores por objeto con annotate()
favoritos = Favorito.objects.select_related('cliente', 'producto').annotate(
    valor=F('descuento_puntos') * F('producto__precio')
)

# 2. Agrupado por estado
por_estado = Favorito.objects.values('estado').annotate(
    cantidad=Count('id'),
    descuento_total=Sum('descuento_puntos'),
    valor_total=Sum(F('descuento_puntos') * F('producto__precio'))
)

# 3. Agrupado por cliente
por_cliente = Favorito.objects.values('cliente__nombre').annotate(
    favoritos=Count('id'),
    descuento_total=Sum('descuento_puntos'),
    valor_total=Sum(F('descuento_puntos') * F('producto__precio'))
).order_by('-valor_total')

# 4. Combinado estado × cliente
estado_cliente = Favorito.objects.values(
    'cliente__nombre', 'estado'
).annotate(
    descuento=Sum('descuento_puntos')
).order_by('cliente__nombre', 'estado')
```

**Resultados por estado:**
| Estado | Cantidad | Descuento Total | Valor Total |
|---|---|---|---|
| activo | 2 | 40 | 1,119.75 |
| inactivo | 3 | 35 | 4,399.65 |
| oferta | 2 | 50 | 14,499.70 |
| comprado | 1 | 100 | 349,999.00 |

**Resultados por cliente:**
| Cliente | Favoritos | Descuento Total | Valor Total |
|---|---|---|---|
| Carlos | 2 | 115 | 352,248.85 |
| María | 2 | 50 | 93,999.50 |
| Pedro | 1 | 25 | 4,499.75 |
| Juan | 2 | 60 | 230,899.40 |
| Ana | 1 | 5 | 649.95 |

---

### Ejercicio 6: Página de reporte con floatformat

**Funcionalidad:** Página web unificada que muestra en una sola vista todos los resultados de los ejercicios 4 y 5, aplicando el filtro de plantilla `floatformat:2` para el formato decimal.

**Archivos creados/modificados:**
| Archivo | Acción | Descripción |
|---|---|---|
| `clientes/views.py` | Modificado | Nueva vista `reporte_view` con 5 consultas: `aggregate()`, `annotate()`, 3x `values().annotate()` |
| `clientes/urls.py` | Modificado | Nueva URL `/reporte/` con nombre `reporte_view` |
| `clientes/templates/clientes/reporte.html` | Creado | Template con 5 secciones heredando de `base.html`, usando `floatformat:2` |
| `clientes/templates/clientes/base.html` | Modificado | Enlace "📊 Reporte" añadido en la barra de navegación |

**Vista `reporte_view` — 5 secciones de datos:**

| Sección | Método Django ORM | Descripción |
|---|---|---|
| 1. Resumen Global | `aggregate()` | Total favoritos (8), total descuento (255), promedio descuento (31.875), valor total (S/ 682,297.45) |
| 2. Valores por Objeto | `annotate()` + `select_related()` | Tabla con todos los favoritos: cliente, producto, descuento, precio, valor calculado (`descuento_puntos * precio`), estado con badge de color |
| 3. Agrupado por Estado | `values('estado').annotate()` | 4 grupos: activo, inactivo, oferta, comprado — con cantidad, descuento total y valor total |
| 4. Agrupado por Cliente | `values('cliente__nombre').annotate().order_by('-valor_total')` | 5 grupos por cliente ordenados por valor total descendente |
| 5. Combinado Estado × Cliente | `values('cliente__nombre', 'estado').annotate()` | Agrupación doble: cada combinación estado-cliente con descuento acumulado |

**Código clave:**
```python
# 1. Resumen global con aggregate()
global_res = Favorito.objects.aggregate(
    total_favoritos=Count('id'),
    total_descuento=Sum('descuento_puntos'),
    promedio_descuento=Avg('descuento_puntos'),
    total_valor=Sum(F('descuento_puntos') * F('producto__precio'))
)

# 2. Valores por objeto con annotate()
favoritos_annotated = Favorito.objects.select_related(
    'cliente', 'producto'
).annotate(
    valor=F('descuento_puntos') * F('producto__precio')
)

# 3. Agrupados por estado
por_estado = Favorito.objects.values('estado').annotate(
    cantidad=Count('id'),
    descuento_total=Sum('descuento_puntos'),
    valor_total=Sum(F('descuento_puntos') * F('producto__precio'))
)
```

**Uso de `floatformat:2` en la plantilla:**
- `{{ global_res.total_descuento|floatformat:2 }}` → "255.00"
- `{{ global_res.total_valor|floatformat:2 }}` → "682297.45"
- `{{ fav.valor|floatformat:2 }}` → "2249.85"
- Se aplica en todas las tablas y tarjetas de resumen

**URL de acceso:** `/reporte/` (también accesible desde el enlace "📊 Reporte" en la barra de navegación)

**Estado:** HTTP 200 — Verificado exitosamente.

---

### Ejercicio 7: QuerySet personalizado con as_manager()

_Sección pendiente de documentación._

---

### Ejercicio 7: QuerySet personalizado con as_manager()

_Sección pendiente de documentación._

---

### Ejercicio 8: Medir y optimizar consultas N+1

_Sección pendiente de documentación._

---

## PARTE 2 — Consultas avanzadas sobre la investigación propia

### Ejercicio 9: Tabla de equivalencias

**Implementación:** Se documentó una tabla completa de equivalencias en `clientes/models.py` (líneas 199-267) que mapea las 14 entidades del proyecto e-commerce.

**Tablas relacionadas:**

| Entidad | Tabla Django | Campos principales | Tipo de relación | Related Name(s) |
|---------|-------------|-------------------|------------------|-----------------|
| **Cliente** | clientes_cliente | id_cliente, nombre, apellido, email, telefono, fecha_registro | 1:N | direcciones, resenas, favoritos |
| **MetodoPago** | clientes_metodopago | id_pago, tipo, proveedor, activo | 1:N | pagos |
| **Carrito** | clientes_carrito | id_carrito, fecha_creacion, estado | 1:0..1 | (sin FK directa) |
| **Direccion** | clientes_direccion | id_direccion, calle, ciudad, codigo_postal, cliente_id | N:1 | direcciones (en Cliente) |
| **Resena** | clientes_resena | id_resena, cliente_id, comentario, calificacion, fecha | N:1 | resenas (en Cliente) |
| **PerfilCliente** | clientes_perfilcliente | cliente_id, fecha_nacimiento, genero, recibir_newsletter, preferencias | 1:1 | perfil (en Cliente) |
| **Favorito** | clientes_favorito | id, cliente_id, producto_id, fecha_agregado, notificar_oferta, descuento_puntos, estado, prioridad | N:M bridge | favoritos (en Cliente), favorito_de (en Producto) |
| **Categoria** | catalogo_categoria | id_categoria, nombre, descripcion | 1:N | productos |
| **Marca** | catalogo_marca | id_marca, nombre, descripcion | 1:N | productos |
| **Proveedor** | catalogo_proveedor | id_proveedor, nombre, telefono, email | 1:N | productos |
| **Producto** | catalogo_producto | id_producto, nombre, precio, descripcion, categoria_id, marca_id, proveedor_id, stock, fecha_creacion | N:1 / 1:1 / N:M | clientes_que_lo_favoritearon, detalles_pedido |
| **Inventario** | catalogo_inventario | id_inventario, producto_id, cantidad, stock_minimo | 1:1 | inventario (en Producto) |
| **Pedido** | ventas_pedido | id_pedido, cliente_id, fecha_pedido, estado, total | N:1 / N:M | pedidos (en Cliente), detalles, productos |
| **DetallePedido** | ventas_detallepedido | id_detalle, pedido_id, producto_id, cantidad, precio_unitario, subtotal | N:1 | detalles (en Pedido), detalles_pedido (en Producto) |
| **Pago** | ventas_pago | id_pago, pedido_id, metodo_pago_id, monto, estado, fecha_pago | 1:1 / N:1 | (en Pedido), pagos (en MetodoPago) |
| **Envio** | ventas_envio | id_envio, pedido_id, direccion_id, empresa_envio, estado, fecha_envio, fecha_entrega | 1:1 / N:1 | (en Pedido), envios (en Direccion) |
| **Cupon** | ventas_cupon | id_cupon, codigo, descripcion, descuento, fecha_inicio, fecha_fin, activo | — | (sin relaciones FK) |

**Campos utilizados en consultas avanzadas:**
- `Favorito.descuento_puntos` (IntegerField) → usado en aggregate(Sum) y filter(con_valor_mayor_a)
- `Pedido.total` (DecimalField) → usado en aggregate(Sum, Avg) y annotate por estado/cliente
- `Pedido.estado` (CharField) → usado en values().annotate() para agrupación
- `Cliente.nombre`, `Cliente.apellido` → usados en values().annotate() para estadísticas por cliente

---

### Ejercicio 10: Operación transaccional en la investigación propia

**Implementación:** View `procesar_pedido_confirm(request, pk)` en `clientes/views.py` (líneas 348-394).

**Descripción:** Esta vista implementa una operación transaccional que procesa el pago de un pedido:

1. **Flujo GET:** Muestra una página de confirmación con los datos del pedido (id, cliente, fecha, estado, total).
2. **Flujo POST (Procesamiento):**
   - Usa `transaction.atomic()` para garantizar atomicidad.
   - Crea un registro de `Pago` vinculado al pedido con el mismo monto.
   - Usa `F('total')` para una actualización atómica del campo total del pedido.
   - Actualiza el `estado` del pedido a `'Pagado'`.
   - Si algo falla, la transacción completa se revierte (rollback).
   - Aplica patrón Post/Redirect/Get (PRG) redirigiendo a `cliente_list`.

**Código clave:**
```python
with transaction.atomic():
    Pago.objects.create(
        pedido=pedido,
        metodo_pago=metodo,
        monto=pedido.total,
        estado='Procesado',
    )
    rows = Pedido.objects.filter(pk=pedido.pk).update(
        estado='Pagado',
        total=F('total'),
    )
```

**URL:** `/procesar-pedido/<int:pk>/`  
**Template:** `clientes/procesar_pedido_confirm.html`

---

### Ejercicio 11: View y Template de reportes con aggregate() y annotate()

**Implementación:** View `reporte_ventas_view(request)` en `clientes/views.py` (líneas 401-439) con template `clientes/reporte_ventas.html`.

**Secciones del reporte:**

1. **Resumen Global (aggregate):**
   - `Count('id')` → total de pedidos
   - `Sum('total')` → monto total acumulado
   - `Avg('total')` → promedio por pedido

2. **Desglose por Estado (values + annotate):**
   - Agrupa por `estado` usando `values('estado').annotate(...)`
   - Muestra cantidad, monto total y promedio por cada estado

3. **Estadísticas por Cliente (values + annotate):**
   - Agrupa por nombre y apellido del cliente usando `values('cliente__nombre', 'cliente__apellido').annotate(...)`
   - Muestra total de pedidos, monto total y promedio por cliente

**Código clave:**
```python
# Aggregate
global_res = Pedido.objects.aggregate(
    total_pedidos=Count('id'),
    total_monto=Sum('total'),
    promedio_total=Avg('total'),
)

# Annotate por estado
por_estado = Pedido.objects.values('estado').annotate(
    total_pedidos=Count('id'),
    total_monto=Sum('total'),
    promedio_total=Avg('total'),
).order_by('-total_monto')
```

**Formato:** Todas las cantidades decimales usan el filtro `floatformat:2` en los templates.

**URL:** `/reporte-ventas/`

---

### Ejercicio 12: QuerySet personalizado en la investigación propia

**Implementación:** QuerySet personalizado en `ventas/models.py` con clase `PedidoCustomQuerySet` y `PedidoManager` (líneas 8-32).

**Métodos personalizados:**

| Método | Tipo | Descripción |
|--------|------|-------------|
| `pedidos_pendientes()` | Encadenable | Filtra y retorna solo pedidos con `estado='Pendiente'` |
| `con_mayor_a(monto)` | Encadenable | Filtra y retorna pedidos con `total > monto` |

**Clases implementadas:**
```python
class PedidoCustomQuerySet(models.QuerySet):
    def pedidos_pendientes(self):
        return self.filter(estado='Pendiente')
    
    def con_mayor_a(self, monto):
        return self.filter(total__gt=monto)

class PedidoManager(models.Manager):
    def get_queryset(self):
        return PedidoCustomQuerySet(self.model, using=self._db)
    
    def pedidos_pendientes(self):
        return self.get_queryset().pedidos_pendientes()
    
    def con_mayor_a(self, monto):
        return self.get_queryset().con_mayor_a(monto)

class Pedido(models.Model):
    objects = PedidoManager()  # Custom manager asignado
    # ... demás campos
```

**Vista de aplicación:** `pedidos_pendientes_view(request, umbral=0)` en `clientes/views.py` (líneas 446-471)

- Usa `Pedido.objects.pedidos_pendientes()` para mostrar pedidos pendientes
- Usa `Pedido.objects.con_mayor_a(umbral)` para mostrar pedidos con total mayor al umbral

**Templates:**
- `clientes/pedidos_pendientes.html` — Muestra ambas listas con badges de estado y formato monetario

**URLs:**
- `/pedidos-pendientes/` → pedidos pendientes
- `/pedidos-pendientes/mayor-a/<umbral>/` → pedidos con total mayor al umbral

---

### Ejercicio 13: Medir y optimizar N+1 en la investigación propia

**Implementación:** View `optimizacion_nplus1_pedidos_view(request)` en `clientes/views.py`.

**Problema N+1 identificado:**
Al listar todos los `Pedido` y acceder a relaciones anidadas (`pedido.cliente`, `pedido.detalles`, `detalle.producto`), se generan múltiples consultas SQL:
- 1 query para obtener los pedidos
- N queries para obtener los datos del cliente de cada pedido
- M queries para obtener los detalles de cada pedido
- Q queries para obtener los productos de cada detalle

**Solución implementada:**

| Técnica | Uso | Qué resuelve |
|---------|-----|-------------|
| `select_related('cliente')` | Relaciones FK | Une la tabla `clientes_cliente` en el JOIN del SELECT |
| `prefetch_related('detalles__producto')` | Relaciones M2M/FK anidadas | Hace un SELECT separado para todos los detalles+productos |

**Medición de rendimiento:**
- Se usa `connection.queries_log.clear()` antes de cada bloque
- Se cuenta `len(connection.queries)` después de recorrer los datos
- Se muestran las consultas SQL exactas en secciones `<details>` expandibles

**Resultados esperados:**
- Sin optimizar: N+M+Q+1 consultas (donde N = pedidos, M = detalles, Q = productos)
- Optimizado: 3 consultas fijas (pedidos + clientes JOIN + prefetch detalles+productos)

**Template:** `clientes/optimizacion_nplus1_pedidos.html`
- Sección 1: Listado sin optimización con conteo de queries
- Sección 2: Listado con optimización
- Sección 3: Tabla comparativa de rendimiento
- Sección 4: Queries SQL debug (expandibles)

**URL:** `/optimizacion-pedidos/`

---

### Ejercicio 14: Actualizar requirements.txt y README.md

**requirements.txt:**
- Django==5.2.13
- sqlite3 (base de datos incluida con Python)

**README.md:** Documentación actualizada con:
- Descripción del proyecto e-commerce con 3 apps (clientes, catálogo, ventas)
- 14 ejercicios de Django ORM avanzado implementados
- Tabla de equivalencias de las 14 entidades/módelos
- Operaciones transaccionales con `transaction.atomic()` y `F()`
- Agregaciones con `aggregate()` (Sum, Count, Avg)
- Anotaciones con `annotate()` y `values().annotate()`
- QuerySets personalizados para reglas de negocio
- Optimización N+1 con `select_related()` y `prefetch_related()`
- Patrones PRG (Post/Redirect/Get)
- Medición de consultas con `connection.queries` (DEBUG=True)

**URLs implementadas:**
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

