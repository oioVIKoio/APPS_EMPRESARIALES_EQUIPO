# Laboratorio N° 07 — Django ORM Avanzado

## PARTE 1 — Consultas avanzadas sobre la aplicación base (Semanas 4 a 6)

- [x] Ejercicio 1: Identificar entidad principal y 3 relaciones. Ubicar/agregar campo entero a descontar, campo de estado y atributo numérico en modelo intermedio N:M.
- [x] Ejercicio 2: Cargar datos de prueba vía Django Admin (5 entidad principal, 3 relación 1:N, 8 modelo intermedio N:M).
- [x] Ejercicio 3: Crear View/URL/Template con transaction.atomic() y F() descontando campo entero. Manejar patrón Post/Redirect/Get y probar caso exitoso y caso con rollback.
- [x] Ejercicio 4: Calcular total global en python manage.py shell usando aggregate() y F() sobre el modelo intermedio.
- [x] Ejercicio 5: Calcular valores por objeto con annotate() y agrupados por estado con values().annotate().
- [x] Ejercicio 6: Crear página de reporte (`reporte.html` heredando de `base.html`) mostrando los resultados de los Ejercicios 4 y 5 con filtros de plantilla (`floatformat`).
- [x] Ejercicio 7: Crear QuerySet personalizado (`as_manager()`) con al menos 2 métodos encadenables de reglas de negocio y aplicarlo en al menos 2 Views.
- [x] Ejercicio 8: Medir consultas (DEBUG=True, connection.queries) en un listado y optimizar el problema N+1 usando select_related() / prefetch_related().

## PARTE 2 — Consultas avanzadas sobre la investigación propia (7 entidades)

- [x] Ejercicio 9: Completar la tabla de equivalencias de la investigación e identificar los campos a utilizar.
- [x] Ejercicio 10: Implementar operación transaccional en la investigación propia con transaction.atomic() y F().
- [x] Ejercicio 11: Crear View y Template de reportes de la investigación propia usando aggregate() y annotate().
- [x] Ejercicio 12: Crear e implementar QuerySet personalizado para la investigación propia en al menos 2 Views.
- [x] Ejercicio 13: Identificar, medir y optimizar la pantalla con más consultas de la investigación (N+1) con select_related/prefetch_related.
- [x] Ejercicio 14: Actualizar requirements.txt y README.md con la documentación del laboratorio.
