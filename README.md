# Tienda Online

Proyecto desarrollado para el curso de **Desarrollo de Aplicaciones Empresariales**.

## Descripción

Sistema web de una tienda online desarrollado con **Django**, utilizando el patrón **MVT**, Django ORM y **SQLite** como base de datos.

El proyecto está dividido en tres aplicaciones:

* `clientes/` — Gestión de clientes.
* `catalogo/` — Gestión del catálogo de productos.
* `ventas/` — Gestión de pedidos y ventas.

## Tecnologías

* Python
* Django
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
```

### 2. Crear entorno virtual

```bash
python -m venv .venv
source .venv/bin/activate.fish
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar migraciones

```bash
python manage.py migrate
```

### 5. Ejecutar el servidor

```bash
python manage.py runserver
```

El proyecto estará disponible en:

`http://127.0.0.1:8000/`

## Estado

🚧 Proyecto en desarrollo — Semana 03.
