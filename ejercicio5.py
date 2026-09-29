# -*- coding: utf-8 -*-
import os
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from clientes.models import Favorito
from django.db.models import F, Sum, Count, Avg

print("=" * 70)
print("EJERCICIO 5: annotate() por objeto y values().annotate() por grupo")
print("=" * 70)

# 1. annotate() por objeto: cada favorito con campos calculados
print("\n1. ANNOTATE() POR OBJETO — Cada favorito con valor calculado:")
print(f"   {'Cliente':<15} {'Producto':<20} {'Descuento':>10} {'Precio':>12} {'Valor':>12} {'Estado':<10}")
print("   " + "-" * 79)
for fav in Favorito.objects.annotate(
    valor=F('descuento_puntos') * F('producto__precio')
):
    valor = fav.descuento_puntos * float(fav.producto.precio)
    estado_label = dict(Favorito._meta.get_field('estado').choices).get(fav.estado, fav.estado)
    print(f"   {fav.cliente.nombre:<15} {fav.producto.nombre:<20} {fav.descuento_puntos:>10} {float(fav.producto.precio):>12.2f} {valor:>12.2f} {estado_label:<10}")

# 2. values().annotate() agrupados por estado
print("\n2. values().annotate() POR ESTADO — Agregados por estado del favorito:")
print(f"   {'Estado':<15} {'Cantidad':>10} {'Descuento Total':>15} {'Precio Total':>15} {'Valor Total':>15}")
print("   " + "-" * 70)
for grupo in Favorito.objects.values('estado').annotate(
    cantidad=Count('id'),
    descuento_total=Sum('descuento_puntos'),
    precio_total=Sum(F('descuento_puntos') * F('producto__precio'))
):
    estado_label = dict(Favorito._meta.get_field('estado').choices).get(grupo['estado'], grupo['estado'])
    print(f"   {estado_label:<15} {grupo['cantidad']:>10} {grupo['descuento_total']:>15.2f} {grupo['precio_total']:>15.2f}")

# 3. values().annotate() agrupados por cliente
print("\n3. values().annotate() POR CLIENTE — Favoritos de cada cliente:")
print(f"   {'Cliente':<15} {'Favoritos':>10} {'Descuento Total':>15} {'Valor Total':>15}")
print("   " + "-" * 55)
for grupo in Favorito.objects.values('cliente__nombre').annotate(
    favoritos=Count('id'),
    descuento_total=Sum('descuento_puntos'),
    valor_total=Sum(F('descuento_puntos') * F('producto__precio'))
).order_by('-valor_total'):
    print(f"   {grupo['cliente__nombre']:<15} {grupo['favoritos']:>10} {grupo['descuento_total']:>15.2f} {grupo['valor_total']:>15.2f}")

# 4. values().annotate() agrupados por estado y cliente (multigrupo)
print("\n4. values().annotate() POR ESTADO y CLIENTE — Combinado:")
print(f"   {'Cliente':<15} {'Estado':<15} {'Descuento':>10} {'Estado Label':<15}")
print("   " + "-" * 55)
for grupo in Favorito.objects.values('cliente__nombre', 'estado').annotate(
    descuento=Sum('descuento_puntos')
).order_by('cliente__nombre', 'estado'):
    estado_label = dict(Favorito._meta.get_field('estado').choices).get(grupo['estado'], grupo['estado'])
    print(f"   {grupo['cliente__nombre']:<15} {grupo['estado']:<15} {grupo['descuento']:>10} {estado_label:<15}")

# 5. Resumen global
print("\n5. RESUMEN GLOBAL:")
global_res = Favorito.objects.aggregate(
    total_favoritos=Count('id'),
    total_descuento=Sum('descuento_puntos'),
    promedio_descuento=Avg('descuento_puntos'),
    total_valor=Sum(F('descuento_puntos') * F('producto__precio'))
)
print(f"   Total favoritos:       {global_res['total_favoritos']}")
print(f"   Descuento total:       {global_res['total_descuento']}")
print(f"   Promedio descuento:    {global_res['promedio_descuento']:.2f}")
print(f"   Valor total (soles):   S/ {global_res['total_valor']:.2f}")

print("\n" + "=" * 70)
print("EJERCICIO 5 COMPLETADO")
print("=" * 70)
