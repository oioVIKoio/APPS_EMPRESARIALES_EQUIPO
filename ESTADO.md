# Bitácora del Laboratorio N° 07

## Última actualización: 2026-09-29 23:00
## Estado actual: En progreso
## Tarea activa: PARTE 2 — Ejercicios 9-14 (investigación)
## Notas/Bloqueos: Ninguno

---

### Historial

| Fecha | Estado | Tarea | Notas |
|---|---|---|---|
| 2026-09-29 21:09 | ✅ Completado | Ejercicio 1 | Migración 0003 generada y aplicada |
| 2026-09-29 21:30 | ✅ Completado | Ejercicio 2 | Script `cargar_datos_prueba.py` — 5 clientes, 8 productos, 8 favoritos |
| 2026-09-29 22:00 | ✅ Completado | Ejercicio 3 | Views `comprar_favorito_confirm/procesar` con `transaction.atomic()` y `F()` |
| 2026-09-29 22:15 | ✅ Completado | Ejercicio 4 | `aggregate()` + `F()` — Total global S/ 682,297.45, 8 favoritos |
| 2026-09-29 22:20 | ✅ Completado | Ejercicio 5 | `annotate()` por objeto + `values().annotate()` por estado/cliente/combinado |
| 2026-09-29 22:30 | ✅ Completado | Ejercicio 6 | Vista `reporte_view`, URL `/reporte/`, plantilla `reporte.html` con 5 secciones y `floatformat:2` |
| 2026-09-29 22:45 | ✅ Completado | Ejercicio 7 | QuerySet `FavoritoCustomQuerySet` con 3 métodos (`favoritos_activos`, `con_valor_mayor_a`, `resumen_por_cliente`), 2 vistas (`favoritos_activos_view`, `favoritos_alto_valor_view`), templates y nav links |
| 2026-09-29 23:00 | ✅ Completado | Ejercicio 8 | Vista `optimizacion_nplus1_view` con `connection.queries`, `select_related()`, template `optimizacion_nplus1.html` con 5 secciones comparativas |
