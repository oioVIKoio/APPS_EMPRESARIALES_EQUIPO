# -*- coding: utf-8 -*-
"""
Script para cargar datos de prueba del Ejercicio 2 - Laboratorio N° 07.

Requisitos:
- 5 clientes (entidad principal)
- 3 categorias, 3 marcas, 3 proveedores (relaciones 1:N del modelo Producto)
- 8 productos (modelo intermedio N:M con Favorito)
- Favoritos vinculando clientes y productos
"""
import os
import sys
import django

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from clientes.models import Cliente, Direccion, Resena, PerfilCliente, Favorito, MetodoPago, Carrito
from catalogo.models import Categoria, Marca, Proveedor, Producto, Inventario


def cargar_datos():
    print("=" * 60)
    print("CARGANDO DATOS DE PRUEBA — Ejercicio 2")
    print("=" * 60)

    # Limpiar datos previos para tener un conteo limpio
    print("\n[PREPARACIÓN] Limpiando datos previos...")
    # Eliminar en orden correcto por dependencias FK (reverse cascade)
    from ventas.models import Envio, Pago, DetallePedido, Pedido, Cupon
    Cupon.objects.all().delete()
    Envio.objects.all().delete()
    Pago.objects.all().delete()
    DetallePedido.objects.all().delete()
    Pedido.objects.all().delete()
    Favorito.objects.all().delete()
    PerfilCliente.objects.all().delete()
    Resena.objects.all().delete()
    Carrito.objects.all().delete()
    Direccion.objects.all().delete()
    MetodoPago.objects.all().delete()
    Cliente.objects.all().delete()
    Inventario.objects.all().delete()
    Producto.objects.all().delete()
    Proveedor.objects.all().delete()
    Marca.objects.all().delete()
    Categoria.objects.all().delete()
    print("  [OK] Base de datos limpia")

    # ── 1. Cargar Categorías (3) ──────────────────────────────
    print("\n[1/8] Creando 3 categorías...")
    categorias = []
    for nombre, desc in [
        ("Electrónica", "Dispositivos y accesorios electrónicos"),
        ("Ropa", "Vestimenta y moda"),
        ("Hogar", "Artículos para el hogar"),
    ]:
        cat, _ = Categoria.objects.get_or_create(nombre=nombre, defaults={"descripcion": desc})
        categorias.append(cat)
    print(f"  [OK] {len(categorias)} categorías: {[c.nombre for c in categorias]}")

    # ── 2. Cargar Marcas (3) ─────────────────────────────────
    print("[2/8] Creando 3 marcas...")
    marcas = []
    for nombre, desc in [
        ("TechBrand", "Marca de tecnología premium"),
        ("FashionCo", "Marca de moda urbana"),
        ("HomePlus", "Marca de hogar y decoración"),
    ]:
        marca, _ = Marca.objects.get_or_create(nombre=nombre, defaults={"descripcion": desc})
        marcas.append(marca)
    print(f"  [OK] {len(marcas)} marcas: {[m.nombre for m in marcas]}")

    # ── 3. Cargar Proveedores (3) ────────────────────────────
    print("[3/8] Creando 3 proveedores...")
    proveedores = []
    for nombre, tel, email in [
        ("TechDist S.A.", "999111222", "contacto@techdist.com"),
        ("FashionImport", "999333444", "ventas@fashionimport.com"),
        ("HogarWorld", "999555666", "info@hogarworld.com"),
    ]:
        prov, _ = Proveedor.objects.get_or_create(
            nombre=nombre, defaults={"telefono": tel, "email": email}
        )
        proveedores.append(prov)
    print(f"  [OK] {len(proveedores)} proveedores: {[p.nombre for p in proveedores]}")

    # ── 4. Cargar Productos (8) ──────────────────────────────
    print("[4/8] Creando 8 productos...")
    productos = []
    datos_productos = [
        ("Laptop Pro 15", 4599.99, categorias[0], marcas[0], proveedores[0], 15),
        ("Smartphone X", 2999.99, categorias[0], marcas[0], proveedores[0], 25),
        ("Camiseta Urban", 89.99, categorias[1], marcas[1], proveedores[1], 50),
        ("Jeans Classic", 149.99, categorias[1], marcas[1], proveedores[1], 40),
        ("Vestido Elegante", 199.99, categorias[1], marcas[1], proveedores[1], 30),
        ("Sofá Moderno", 3499.99, categorias[2], marcas[2], proveedores[2], 8),
        ("Lámpara LED", 129.99, categorias[2], marcas[2], proveedores[2], 60),
        ("Set de Sábanas", 179.99, categorias[2], marcas[2], proveedores[2], 45),
    ]
    for nombre, precio, cat, marca, prov, stock in datos_productos:
        prod, _ = Producto.objects.get_or_create(
            nombre=nombre,
            defaults={
                "descripcion": f"Producto {nombre} de prueba",
                "precio": precio,
                "categoria": cat,
                "marca": marca,
                "proveedor": prov,
            },
        )
        # Crear/actualizar inventario
        inv, _ = Inventario.objects.get_or_create(
            producto=prod,
            defaults={"cantidad": stock, "stock_minimo": 5},
        )
        inv.cantidad = stock
        inv.save()
        productos.append(prod)
    print(f"  [OK] {len(productos)} productos creados")

    # ── 5. Cargar Clientes (5) ───────────────────────────────
    print("[5/8] Creando 5 clientes...")
    clientes = []
    datos_clientes = [
        ("Juan", "Pérez", "juan@email.com", "987654321"),
        ("María", "García", "maria@email.com", "987654322"),
        ("Carlos", "López", "carlos@email.com", "987654323"),
        ("Ana", "Martínez", "ana@email.com", "987654324"),
        ("Pedro", "Rodríguez", "pedro@email.com", "987654325"),
    ]
    for nombre, apellido, email, tel in datos_clientes:
        cli, _ = Cliente.objects.get_or_create(
            email=email,
            defaults={"nombre": nombre, "apellido": apellido, "telefono": tel},
        )
        clientes.append(cli)
    print(f"  [OK] {len(clientes)} clientes creados")

    # ── 6. Crear Perfiles de Cliente ─────────────────────────
    print("[6/8] Creando perfiles de cliente...")
    for i, cliente in enumerate(clientes):
        perfil, _ = PerfilCliente.objects.get_or_create(
            cliente=cliente,
            defaults={
                "fecha_nacimiento": f"1990-{(i+1):02d}-15",
                "genero": ["Masculino", "Femenino", "Masculino", "Femenino", "Masculino"][i],
                "recibir_newsletter": i % 2 == 0,
                "preferencias": f"Preferencias de {cliente.nombre}",
            },
        )
    print(f"  [OK] {len(clientes)} perfiles creados")

    # ── 7. Crear Direcciones ─────────────────────────────────
    print("[7/8] Creando direcciones...")
    direcciones_data = [
        ("Av. Principal 123", "Lima", "15001"),
        ("Calle Secondary 456", "Arequipa", "04001"),
        ("Jr. Comercio 789", "Trujillo", "13001"),
        ("Av. del Sol 321", "Cusco", "08001"),
        ("Calle Los Olivos 654", "Lima", "15002"),
    ]
    for cliente, (calle, ciudad, cp) in zip(clientes, direcciones_data):
        Direccion.objects.get_or_create(
            cliente=cliente,
            defaults={"calle": calle, "ciudad": ciudad, "codigo_postal": cp},
        )
    print(f"  [OK] {len(clientes)} direcciones creadas")

    # ── 8. Crear Favoritos (8) — modelo intermedio N:M ───────
    print("[8/8] Creando 8 favoritos...")
    favoritos_data = [
        (0, 0, True, 50, "activo", 1),   # Juan → Laptop, descuento=50, prioridad=1
        (0, 2, False, 10, "activo", 2),   # Juan → Camiseta
        (1, 1, True, 30, "activo", 1),    # María → Smartphone
        (1, 4, True, 20, "oferta", 2),    # María → Vestido (en oferta)
        (2, 3, False, 15, "inactivo", 3),  # Carlos → Jeans (inactivo)
        (2, 5, True, 100, "activo", 1),    # Carlos → Sofá
        (3, 6, False, 5, "activo", 2),     # Ana → Lámpara
        (4, 7, True, 25, "oferta", 1),     # Pedro → Sábanas (en oferta)
    ]
    favoritos = []
    for idx, (cli_idx, prod_idx, notificar, descuento, estado, prioridad) in enumerate(favoritos_data):
        fav, _ = Favorito.objects.get_or_create(
            cliente=clientes[cli_idx],
            producto=productos[prod_idx],
            defaults={
                "notificar_oferta": notificar,
                "descuento_puntos": descuento,
                "estado": estado,
                "prioridad": prioridad,
            },
        )
        favoritos.append(fav)
    print(f"  [OK] {len(favoritos)} favoritos creados")

    # ── 9. Crear Métodos de Pago ─────────────────────────────
    print("[BONUS] Creando métodos de pago...")
    metodos_data = [
        ("Tarjeta de Crédito", "Visa", True),
        ("Transferencia", "BCP", True),
        ("Yape", "Yape", True),
        ("PayPal", "PayPal", False),
    ]
    for tipo, proveedor, activo in metodos_data:
        MetodoPago.objects.get_or_create(
            tipo=tipo, defaults={"proveedor": proveedor, "activo": activo}
        )
    print(f"  [OK] {len(metodos_data)} métodos de pago")

    # ── Resumen ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    print(f"  Categorías : {Categoria.objects.count()}")
    print(f"  Marcas     : {Marca.objects.count()}")
    print(f"  Proveedores: {Proveedor.objects.count()}")
    print(f"  Productos  : {Producto.objects.count()}")
    print(f"  Clientes   : {Cliente.objects.count()}")
    print(f"  Perfiles   : {PerfilCliente.objects.count()}")
    print(f"  Direcciones: {Direccion.objects.count()}")
    print(f"  Favoritos  : {Favorito.objects.count()}")
    print(f"  Métodos Pago: {MetodoPago.objects.count()}")
    print("=" * 60)
    print("¡Datos de prueba cargados exitosamente!")
    print("Puedes verificarlos en http://127.0.0.1:8000/admin/")
    print("=" * 60)


if __name__ == "__main__":
    cargar_datos()
