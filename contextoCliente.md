# Contexto Completo de la App `clientes`

## Estructura del Directorio

```
clientes/
+-- __init__.py           Archivo vacio, marca el directorio como paquete Python
+-- apps.py               Configuracion de la aplicacion Django
+-- models.py             7 modelos de base de datos
+-- admin.py              Panel de administracion personalizado
+-- views.py              14 vistas (CRUD + listas)
+-- urls.py               17 rutas URL
+-- forms.py              1 formulario (FavoritoForm)
+-- tests.py              Test vacio (sin tests implementados)
+-- __pycache__/          Archivos compilados de Python (bytecode)
+-- migrations/
|   +-- __init__.py
|   +-- 0001_initial.py       Crea: Carrito, Cliente, MetodoPago, Direccion, Resena
|   +-- 0002_favorito_cliente_productos_favoritos_perfilcliente.py Agrega: Favorito, PerfilCliente, ManyToMany
+-- templates/
    +-- clientes/
        +-- base.html
        +-- _cliente_campos.html          Template parcial
        +-- _cliente_resumen.html         Template parcial
        +-- listar_clientes.html
        +-- crear_cliente.html
        +-- editar_cliente.html
        +-- confirmar_eliminar.html
        +-- cliente_perfil.html
        +-- cliente_favoritos.html
        +-- metodo_pago_list.html
        +-- carrito_list.html
        +-- direccion_list.html
        +-- resena_list.html
        +-- favorito_form.html
        +-- favorito_confirm_delete.html
```

---

## Contenido de cada Archivo

### 1. __init__.py
- Estado: Vacio (0 lineas)
- Funcion: Marca al directorio como un paquete Python, permitiendo importaciones de otros modulos dentro de la app.

---

### 2. apps.py
- Contenido: Define ClientesConfig(AppConfig) con name = 'clientes'.
- Funcion: Configuracion estandar que Django registra automaticamente en INSTALLED_APPS.

```python
from django.apps import AppConfig

class ClientesConfig(AppConfig):
    name = 'clientes'
```

---

### 3. models.py - 7 Modelos de Base de Datos

#### 3.1. Cliente
- Descripcion: Modelo principal para gestionar la informacion de clientes.
- Campos:
  - id_cliente -> BigAutoField (Primary Key)
  - nombre -> CharField(max_length=100)
  - apellido -> CharField(max_length=100)
  - email -> EmailField(unique=True)
  - telefono -> CharField(max_length=15)
  - fecha_registro -> DateTimeField(auto_now_add=True)
- Relaciones:
  - ManyToMany con catalogo.Producto a traves de la tabla intermedia Favorito
  - Related name: clientes_que_lo_favoritearon
- Metadatos (class Meta):
  - verbose_name = "Cliente"
  - verbose_name_plural = "Clientes"
- Representacion (__str__): f"{self.nombre} {self.apellido} ({self.email})"

#### 3.2. MetodoPago
- Descripcion: Modelo para gestionar los metodos de pago disponibles.
- Campos:
  - id_pago -> BigAutoField (Primary Key)
  - tipo -> CharField(max_length=50)
  - proveedor -> CharField(max_length=50)
  - activo -> BooleanField(default=True)
- Relaciones: Ninguna directa en esta app (solo se referencia desde la app ventas).
- Metadatos (class Meta):
  - verbose_name = "Metodo de Pago"
  - verbose_name_plural = "Metodos de Pago"
- Representacion (__str__): f"{self.tipo} - {self.proveedor}"

#### 3.3. Carrito
- Descripcion: Modelo para gestionar los carritos de compra.
- Campos:
  - id_carrito -> BigAutoField (Primary Key)
  - fecha_creacion -> DateTimeField(auto_now_add=True)
  - estado -> CharField(max_length=20, default='Activo')
- Relaciones: Ninguna definida (sin FK ni ManyToMany).
- Metadatos (class Meta):
  - verbose_name = "Carrito"
  - verbose_name_plural = "Carritos"
- Representacion (__str__): f"Carrito {self.id_carrito} - {self.estado}"

#### 3.4. Direccion
- Descripcion: Modelo para gestionar direcciones asociadas a clientes.
- Campos:
  - id_direccion -> BigAutoField (Primary Key)
  - calle -> CharField(max_length=200)
  - ciudad -> CharField(max_length=100)
  - codigo_postal -> CharField(max_length=10)
  - cliente -> ForeignKey(Cliente, on_delete=CASCADE, related_name='direcciones')
- Relaciones:
  - ForeignKey -> Cliente (cada direccion pertenece a un cliente)
- Metadatos (class Meta):
  - verbose_name = "Direccion"
  - verbose_name_plural = "Direcciones"
- Representacion (__str__): f"{self.calle}, {self.ciudad} ({self.codigo_postal}) - {self.cliente.nombre}"

#### 3.5. Resena
- Descripcion: Modelo para gestionar reseñas y valoraciones de clientes.
- Campos:
  - id_resena -> BigAutoField (Primary Key)
  - cliente -> ForeignKey(Cliente, on_delete=CASCADE, related_name='resenas')
  - comentario -> TextField()
  - calificacion -> IntegerField()
  - fecha -> DateField(auto_now_add=True)
- Relaciones:
  - ForeignKey -> Cliente (cada resena es de un cliente)
- Metadatos (class Meta):
  - verbose_name = "Resena"
  - verbose_name_plural = "Resenas"
- Representacion (__str__): f"Resena de {self.cliente.nombre} - Calificacion: {self.calificacion}/5"

#### 3.6. PerfilCliente
- Descripcion: Extension del perfil del cliente con datos adicionales.
- Campos:
  - cliente -> OneToOneField(Cliente, on_delete=CASCADE, related_name='perfil')
  - fecha_nacimiento -> DateField(null=True, blank=True)
  - genero -> CharField(max_length=20, blank=True)
  - recibir_newsletter -> BooleanField(default=True)
  - preferencias -> TextField(blank=True)
- Relaciones:
  - OneToOne -> Cliente (perfil extendido del cliente)
- Metadatos (class Meta): No definido (usa los valores por defecto de Django)
- Representacion (__str__): f"Perfil de {self.cliente.nombre}"

#### 3.7. Favorito
- Descripcion: Tabla intermedia entre Cliente y Producto para la relacion ManyToMany.
- Campos:
  - id -> BigAutoField (Primary Key, generado automaticamente)
  - cliente -> ForeignKey(Cliente, on_delete=CASCADE, related_name='favoritos')
  - producto -> ForeignKey('catalogo.Producto', on_delete=CASCADE, related_name='favorito_de')
  - fecha_agregado -> DateTimeField(auto_now_add=True)
  - notificar_oferta -> BooleanField(default=False)
- Relaciones:
  - ForeignKey -> Cliente
  - ForeignKey -> Producto (app catalogo)
- Metadatos (class Meta):
  - unique_together = ('cliente', 'producto') (un cliente no puede tener el mismo producto duplicado en favoritos)
- Representacion (__str__): f"{self.cliente.nombre} {self.producto.nombre}"

---

### 4. admin.py - Panel de Administracion

Registra 7 modelos con configuraciones personalizadas:

#### 4.1. PerfilClienteInline
- Tipo: StackedInline (campos apilados verticalmente en el admin de Cliente)
- Modelo: PerfilCliente
- extra = 0 (no muestra formularios vacios)
- max_num = 1 (solo permite un perfil por cliente)

#### 4.2. FavoritoInline
- Tipo: TabularInline (tabla horizontal en el admin de Cliente)
- Modelo: Favorito
- extra = 0 (no muestra formularios vacios)
- fields = ('producto', 'fecha_agregado', 'notificar_oferta')
- readonly_fields = ('fecha_agregado',)

#### 4.3. ClienteAdmin
- Decorador: @admin.register(Cliente)
- Inlines: [PerfilClienteInline, FavoritoInline]
- list_display: ('id_cliente', 'nombre', 'apellido', 'email', 'telefono', 'fecha_registro')
- search_fields: ('nombre', 'apellido', 'email')
- list_filter: ('fecha_registro',)

#### 4.4. DireccionAdmin
- Decorador: @admin.register(Direccion)
- list_display: ('id_direccion', 'cliente', 'calle', 'ciudad', 'codigo_postal')
- search_fields: ('cliente__nombre', 'cliente__apellido', 'ciudad', 'codigo_postal')

#### 4.5. ResenaAdmin
- Decorador: @admin.register(Resena)
- list_display: ('id_resena', 'cliente', 'calificacion', 'fecha')
- search_fields: ('cliente__nombre', 'cliente__apellido', 'comentario')
- list_filter: ('calificacion', 'fecha')

#### 4.6. Registro basico (sin configuraciones especiales)
- admin.site.register(PerfilCliente)
- admin.site.register(Favorito)
- admin.site.register(MetodoPago)
- admin.site.register(Carrito)

---

### 5. views.py - 14 Vistas

#### 5.1. cliente_list(request)
- Ruta: /clientes/
- Funcion: Lista todos los clientes.
- Template: clientes/listar_clientes.html
- Datos: Clientes.objects.all()

#### 5.2. cliente_detail(request, pk)
- Ruta: /clientes/<int:pk>/
- Funcion: Muestra el detalle de un cliente especifico.
- Template: clientes/listar_clientes.html
- Datos: Clientes.objects.get(pk=pk)

#### 5.3. cliente_create(request)
- Ruta: /clientes/crear/
- Funcion: Crea un nuevo cliente (GET/POST).
- Template: clientes/crear_cliente.html
- Lógica:
  - POST: Lee nombre, apellido, email, telefono del POST, guarda y redirige a cliente_list
  - GET: Renderiza el formulario

#### 5.4. cliente_update(request, pk)
- Ruta: /clientes/<int:pk>/editar/
- Funcion: Edita un cliente existente (GET/POST).
- Template: clientes/editar_cliente.html
- Datos: Clientes.objects.get(pk=pk)
- Lógica:
  - POST: Actualiza nombre, apellido, email, telefono y guarda, redirige a cliente_list
  - GET: Renderiza formulario con datos del cliente

#### 5.5. cliente_delete(request, pk)
- Ruta: /clientes/<int:pk>/eliminar/
- Funcion: Elimina un cliente (GET/POST).
- Template: clientes/confirmar_eliminar.html
- Datos: Clientes.objects.get(pk=pk)
- Lógica:
  - POST: Elimina el cliente y redirige a cliente_list
  - GET: Muestra confirmacion

#### 5.6. metodo_pago_list(request)
- Ruta: /metodos-pago/
- Funcion: Lista todos los metodos de pago.
- Template: clientes/metodo_pago_list.html
- Datos: MetodoPago.objects.all()

#### 5.7. carrito_list(request)
- Ruta: /carritos/
- Funcion: Lista todos los carritos.
- Template: clientes/carrito_list.html
- Datos: Carrito.objects.all()

#### 5.8. direccion_list(request)
- Ruta: /direcciones/
- Funcion: Lista todas las direcciones con optimizacion SQL.
- Template: clientes/direccion_list.html
- Datos: Direccion.objects.select_related('cliente').all()
- Optimizacion: select_related('cliente') - evita queries N+1 para traer la informacion del cliente asociado

#### 5.9. resena_list(request)
- Ruta: /resenas/
- Funcion: Lista todas las resenas.
- Template: clientes/resena_list.html
- Datos: Resena.objects.all()

#### 5.10. cliente_perfil_detail(request, pk)
- Ruta: /cliente/<int:pk>/perfil/
- Funcion: Muestra los detalles del perfil de un cliente.
- Template: clientes/cliente_perfil.html
- Datos: get_object_or_404(Cliente.objects.select_related('perfil'), pk=pk)
- Optimizacion: select_related('perfil') - evita query adicional para obtener el perfil OneToOne

#### 5.11. cliente_favoritos_list(request, pk)
- Ruta: /cliente/<int:pk>/favoritos/
- Funcion: Lista los favoritos de un cliente con sus productos.
- Template: clientes/cliente_favoritos.html
- Datos: get_object_or_404(Cliente.objects.prefetch_related('favoritos__producto'), pk=pk)
- Optimizacion: prefetch_related('favoritos__producto') - prefetch para ManyToMany con tabla intermedia

#### 5.12. favorito_create(request)
- Ruta: /favoritos/crear/
- Funcion: Crea un nuevo favorito (GET/POST).
- Template: clientes/favorito_form.html
- Formulario: FavoritoForm
- Lógica:
  - POST: Valida y guarda el formulario, redirige a cliente_favoritos_list
  - GET: Renderiza formulario, puede recibir producto como parametro GET para precargar

#### 5.13. favorito_update(request, pk)
- Ruta: /favoritos/<int:pk>/editar/
- Funcion: Edita un favorito existente (GET/POST).
- Template: clientes/favorito_form.html
- Formulario: FavoritoForm(instance=favorito)
- Lógica:
  - POST: Valida y guarda cambios, redirige a cliente_favoritos_list
  - GET: Renderiza formulario con datos del favorito

#### 5.14. favorito_delete(request, pk)
- Ruta: /favoritos/<int:pk>/eliminar/
- Funcion: Elimina un favorito (GET/POST).
- Template: clientes/favorito_confirm_delete.html
- Lógica:
  - POST: Elimina y redirige a cliente_favoritos_list del cliente asociado
  - GET: Muestra confirmacion

---

### 6. urls.py - 17 Rutas URL

#### Grupo 1: CRUD de Clientes (6 rutas)
| Ruta | Vista | Nombre |
|---|---|---|
| clientes/ | views.cliente_list | cliente_list |
| clientes/crear/ | views.cliente_create | crear_cliente |
| clientes/editar/ | RedirectView.as_view(pattern_name='cliente_list', permanent=False) | (sin nombre) |
| clientes/<int:pk>/ | views.cliente_detail | cliente_detail |
| clientes/<int:pk>/editar/ | views.cliente_update | editar_cliente |
| clientes/<int:pk>/eliminar/ | views.cliente_delete | eliminar_cliente |

#### Grupo 2: Listados de otras entidades (4 rutas)
| Ruta | Vista | Nombre |
|---|---|---|
| metodos-pago/ | views.metodo_pago_list | metodo_pago_list |
| carritos/ | views.carrito_list | carrito_list |
| direcciones/ | views.direccion_list | direccion_list |
| resenas/ | views.resena_list | resena_list |

#### Grupo 3: Vistas con optimizacion de relaciones (2 rutas)
| Ruta | Vista | Nombre |
|---|---|---|
| cliente/<int:pk>/perfil/ | views.cliente_perfil_detail | cliente_perfil_detail |
| cliente/<int:pk>/favoritos/ | views.cliente_favoritos_list | cliente_favoritos_list |

#### Grupo 4: CRUD de Favoritos (3 rutas)
| Ruta | Vista | Nombre |
|---|---|---|
| favoritos/crear/ | views.favorito_create | favorito_create |
| favoritos/<int:pk>/editar/ | views.favorito_update | favorito_update |
| favoritos/<int:pk>/eliminar/ | views.favorito_delete | favorito_delete |

Importacion: from django.urls import path, from django.views.generic import RedirectView, from . import views

---

### 7. forms.py - 1 Formulario

#### FavoritoForm(forms.ModelForm)
- Modelo base: Favorito
- Campos: ['cliente', 'producto', 'notificar_oferta']
- Widgets personalizados:
  - cliente: forms.Select(attrs={'class': 'form-select'})
  - producto: forms.Select(attrs={'class': 'form-select'})
  - notificar_oferta: forms.CheckboxInput(attrs={'class': 'form-check-input'})

---

### 8. tests.py - Sin Tests Implementados

Solo contiene:
```python
from django.test import TestCase
# Create your tests here.
```
No hay pruebas escritas.

---

### 9. migrations/ - Historial de Migraciones

#### Migracion 1: 0001_initial.py
- Generado por: Django 5.2.13
- Fecha: 2026-09-02 02:41
- Dependencias: Ninguna (inicio de la app)
- Operaciones (CreateModel):
  1. Carrito: id_carrito (PK), fecha_creacion, estado (default='Activo')
  2. Cliente: id_cliente (PK), nombre, apellido, email (unico), telefono, fecha_registro
  3. MetodoPago: id_pago (PK), tipo, proveedor, activo (default=True)
  4. Direccion: id_direccion (PK), calle, ciudad, codigo_postal, cliente (FK -> Cliente)
  5. Resena: id_resena (PK), comentario, calificacion, fecha, cliente (FK -> Cliente)

#### Migracion 2: 0002_favorito_cliente_productos_favoritos_perfilcliente.py
- Generado por: Django 5.2.13
- Fecha: 2026-09-09 14:18
- Dependencias: ('catalogo', '0003_alter_categoria_id_alter_inventario_id_and_more'), ('clientes', '0001_initial')
- Operaciones:
  1. CreateModel Favorito: id (PK auto), fecha_agregado, notificar_oferta (default=False), cliente (FK -> Cliente), producto (FK -> catalogo.Producto)
     - unique_together = ('cliente', 'producto')
  2. AddField Cliente.productos_favoritos: ManyToManyField a catalogo.Producto con through='clientes.Favorito', related_name='clientes_que_lo_favoritearon'
  3. CreateModel PerfilCliente: id (PK auto), fecha_nacimiento (nullable, blank), genero (blank), recibir_newsletter (default=True), preferencias (blank), cliente (OneToOneField -> Cliente)

---

### 10. templates/clientes/ - 15 Plantillas HTML

| Archivo | Tipo | Uso |
|---|---|---|
| base.html | Base | Plantilla padre para herencia de plantillas |
| _cliente_campos.html | Parcial (_) | Renderiza campos de formulario de cliente |
| _cliente_resumen.html | Parcial (_) | Muestra resumen de informacion de cliente |
| listar_clientes.html | Principal | Listado de clientes |
| crear_cliente.html | Principal | Formulario para crear cliente |
| editar_cliente.html | Principal | Formulario para editar cliente |
| confirmar_eliminar.html | Principal | Confirmacion para eliminar cliente |
| cliente_perfil.html | Principal | Detalle del perfil de un cliente |
| cliente_favoritos.html | Principal | Listado de favoritos de un cliente |
| metodo_pago_list.html | Principal | Listado de metodos de pago |
| carrito_list.html | Principal | Listado de carritos |
| direccion_list.html | Principal | Listado de direcciones |
| resena_list.html | Principal | Listado de resenas |
| favorito_form.html | Principal | Formulario para CRUD de favoritos (crear/editar) |
| favorito_confirm_delete.html | Principal | Confirmacion para eliminar favorito |

Convencion de naming:
- Archivos que comienzan con _ (como _cliente_campos.html y _cliente_resumen.html) son templates parciales que se incluyen desde otros templates, no se sirven directamente.

---

## Relaciones entre Modelos

```
+--------------+
|   Cliente    |
+--------------+
| id_cliente (PK)
| nombre
| apellido
| email (unique)
| telefono
| fecha_registro
+------+-------+
       |
       | 1:N -------------------------+
       | OneToOne                     |
       v                              v
+--------------+      +------------------+
| PerfilCliente|      |   Direccion      |
+--------------+      +------------------+
| cliente (PK) |      | id_direccion (PK)|
| fecha_nac.   |      | calle            |
| genero       |      | ciudad           |
| newsletter   |      | codigo_postal    |
| preferencias |      | cliente (FK)-----+
+--------------+

       |
       | M:N (via Favorito)
       v
+------------------+      +--------------+
|    Favorito      |      |  Resena      |
+------------------+      +--------------+
| id (PK)          |      | id_resena(PK)|
| cliente (FK)-----+--+   | cliente(FK)--+--+
| producto (FK)----+  |   | comentario   |  |
| fecha_agregado   |   |   | calificacion |  |
| notificar_oferta |   |   | fecha        |  |
+------------------+   +--------------+  |
       |                                 |
       | (FK a catalogo.Producto)        |
       v                                 |
+------------------+                     |
|  catalogo.Producto|                    |
+------------------+                     |
                                         |
                          +--------------+
                          |
                   +--------------+
                   |   MetodoPago  |
                   +--------------+
                   | id_pago (PK) |
                   | tipo         |
                   | proveedor    |
                   | activo       |
                   +--------------+

                   +--------------+
                   |    Carrito   |
                   +--------------+
                   | id_carrito(PK)|
                   | fecha_creacion|
                   | estado       |
                   +--------------+
```

---

## Resumen de Entidades (Tablas)

| # | Modelo | Tabla en BD | Campos | Tipo de Relacion |
|---|---|---|---|---|
| 1 | Cliente | clientes_cliente | id_cliente, nombre, apellido, email, telefono, fecha_registro | Base de todas las relaciones |
| 2 | MetodoPago | clientes_metodopago | id_pago, tipo, proveedor, activo | Ninguna directa |
| 3 | Carrito | clientes_carrito | id_carrito, fecha_creacion, estado | Ninguna directa |
| 4 | Direccion | clientes_direccion | id_direccion, calle, ciudad, codigo_postal, cliente_id | FK -> Cliente (1:N) |
| 5 | Resena | clientes_resena | id_resena, cliente_id, comentario, calificacion, fecha | FK -> Cliente (1:N) |
| 6 | PerfilCliente | clientes_perfilcliente | id, cliente_id, fecha_nacimiento, genero, recibir_newsletter, preferencias | OneToOne -> Cliente (1:1) |
| 7 | Favorito | clientes_favorito | id, cliente_id, producto_id, fecha_agregado, notificar_oferta | FK -> Cliente + FK -> Producto (tabla intermedia) |

---

## Optimizaciones SQL Utilizadas

| Vista | Optimizacion | Proposito |
|---|---|---|
| direccion_list | select_related('cliente') | Evitar N+1 queries al acceder direccion.cliente |
| cliente_perfil_detail | select_related('perfil') | Evitar query extra al acceder cliente.perfil |
| cliente_favoritos_list | prefetch_related('favoritos__producto') | Evitar N+1 queries al acceder fav.producto en ManyToMany |

---

## Importaciones y Dependencias

### models.py
```python
from django.db import models
```

### admin.py
```python
from django.contrib import admin
from .models import (Cliente, PerfilCliente, Direccion, Favorito, Resena, MetodoPago, Carrito)
```

### views.py
```python
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, MetodoPago, Carrito, Direccion, Resena, PerfilCliente, Favorito
from .forms import FavoritoForm
```

### urls.py
```python
from django.urls import path
from django.views.generic import RedirectView
from . import views
```

### forms.py
```python
from django import forms
from .models import Favorito
```

### tests.py
```python
from django.test import TestCase
```

### apps.py
```python
from django.apps import AppConfig
```

---

## Configuracion en el Proyecto Principal

La app clientes esta registrada en config/settings.py dentro de INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'clientes',     # Esta app
    'catalogo',     # App relacionada
    'ventas',       # App relacionada
]
```

---

## Interacciones con Otras Apps

| App Destino | Modelo Destino | Tipo de Relacion | Desde... |
|---|---|---|---|
| catalogo | Producto | ForeignKey (en Favorito) | clientes |
| catalogo | Producto | ManyToMany (via Favorito) | clientes |
| clientes | Cliente | ForeignKey (desde ventas.Pedido) | ventas |
| clientes | Direccion | ForeignKey (desde ventas.Envio) | ventas |
| clientes | MetodoPago | ForeignKey (desde ventas.Pago) | ventas |

---

## Funcionalidades CRUD Implementadas

| Entidad | Listar | Detalle | Crear | Editar | Eliminar |
|---|---|---|---|---|---|
| Cliente | OK | OK | OK | OK | OK |
| Direccion | OK | NO | NO | NO | NO |
| Resena | OK | NO | NO | NO | NO |
| MetodoPago | OK | NO | NO | NO | NO |
| Carrito | OK | NO | NO | NO | NO |
| PerfilCliente | NO (solo via detalle de Cliente) | OK (via /cliente/<pk>/perfil/) | NO (via Inline en admin) | NO | NO |
| Favorito | OK | NO | OK | OK | OK |

---

## Observaciones y Notas

1. clientes/editar/ en urls.py es un redirect a cliente_list (placeholder sin funcionalidad real).
2. tests.py no tiene pruebas implementadas.
3. La app MetodoPago y Carrito no tienen relaciones definidas con otros modelos en la app clientes.
4. El archivo __init__.py esta vacio.
5. La dependencia cruzada con la app catalogo se establece a traves de Favorito (ForeignKey a catalogo.Producto).
6. Todos los modelos usan BigAutoField como primary key explícito excepto PerfilCliente y Favorito que usan el auto-generado.
7. PerfilCliente no tiene class Meta definido.
8. La migracion 0002 depende de la app catalogo (migracion 0003).
9. La app usa plantillas organizadas con templates parciales para reutilizacion.
