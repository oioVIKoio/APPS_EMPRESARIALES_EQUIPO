from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction, models
from django.db import connection
from django.db.models import F, Sum, Count, Avg
from django.contrib import messages
from .models import Cliente, MetodoPago, Carrito, Direccion, Resena, PerfilCliente, Favorito
from .forms import FavoritoForm
from catalogo.models import Inventario
from ventas.models import Pedido

def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/listar_clientes.html', {'clientes': clientes})


def cliente_detail(request, pk):
    cliente = Cliente.objects.get(pk=pk)
    return render(request, 'clientes/listar_clientes.html', {'clientes': [cliente]})


def cliente_create(request):
    if request.method == 'POST':
        cliente = Cliente(
            nombre=request.POST.get('nombre'),
            apellido=request.POST.get('apellido'),
            email=request.POST.get('email'),
            telefono=request.POST.get('telefono')
        )
        cliente.save()
        return redirect('cliente_list')

    return render(request, 'clientes/crear_cliente.html')


def cliente_update(request, pk):
    cliente = Cliente.objects.get(pk=pk)

    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre')
        cliente.apellido = request.POST.get('apellido')
        cliente.email = request.POST.get('email')
        cliente.telefono = request.POST.get('telefono')
        cliente.save()
        return redirect('cliente_list')

    return render(request, 'clientes/editar_cliente.html', {'cliente': cliente})


def cliente_delete(request, pk):
    cliente = Cliente.objects.get(pk=pk)

    if request.method == 'POST':
        cliente.delete()
        return redirect('cliente_list')

    return render(request, 'clientes/confirmar_eliminar.html', {'cliente': cliente})


def metodo_pago_list(request):
    metodos = MetodoPago.objects.all()
    return render(request, 'clientes/metodo_pago_list.html', {'metodos': metodos})


def carrito_list(request):
    carritos = Carrito.objects.all()
    return render(request, 'clientes/carrito_list.html', {'carritos': carritos})


def direccion_list(request):
    # Optimización 1:N con select_related para traer la información del cliente
    direcciones = Direccion.objects.select_related('cliente').all()
    return render(request, 'clientes/direccion_list.html', {'direcciones': direcciones})


def resena_list(request):
    resenas = Resena.objects.all()
    return render(request, 'clientes/resena_list.html', {'resenas': resenas})       
    
def cliente_perfil_detail(request, pk):
    cliente = get_object_or_404(
        Cliente.objects.select_related('perfil'), 
        pk=pk
    )
    return render(request, 'clientes/cliente_perfil.html', {'cliente': cliente})


def cliente_favoritos_list(request, pk):

    cliente = get_object_or_404(
        Cliente.objects.prefetch_related('favoritos__producto'), 
        pk=pk
    )
    return render(request, 'clientes/cliente_favoritos.html', {'cliente': cliente})

def favorito_create(request):
    if request.method == 'POST':
        form = FavoritoForm(request.POST)
        if form.is_valid():
            fav = form.save()
            return redirect('cliente_favoritos_list', pk=fav.cliente.pk)
    else:
        producto_id = request.GET.get('producto')
        initial = {'producto': producto_id} if producto_id else None
        form = FavoritoForm(initial=initial)
    return render(request, 'clientes/favorito_form.html', {'form': form, 'titulo': 'Agregar a Favoritos'})

def favorito_update(request, pk):
    favorito = get_object_or_404(Favorito, pk=pk)
    if request.method == 'POST':
        form = FavoritoForm(request.POST, instance=favorito)
        if form.is_valid():
            form.save()
            return redirect('cliente_favoritos_list', pk=favorito.cliente.pk)
    else:
        form = FavoritoForm(instance=favorito)
    return render(request, 'clientes/favorito_form.html', {'form': form, 'titulo': 'Editar Favorito'})

def favorito_delete(request, pk):
    favorito = get_object_or_404(Favorito, pk=pk)
    cliente_pk = favorito.cliente.pk
    if request.method == 'POST':
        favorito.delete()
        return redirect('cliente_favoritos_list', pk=cliente_pk)
    return render(request, 'clientes/favorito_confirm_delete.html', {'favorito': favorito})


def comprar_favorito_confirm(request, pk):
    """Muestra confirmación para comprar un producto favorito."""
    favorito = get_object_or_404(Favorito, pk=pk)
    producto = favorito.producto
    inventario = favorito.producto.inventario  # OneToOne con related_name
    context = {
        'favorito': favorito,
        'producto': producto,
        'inventario': inventario,
        'descuento': favorito.descuento_puntos,
    }
    return render(request, 'clientes/comprar_favorito_confirm.html', context)


def comprar_favorito_procesar(request, pk):
    """Procesa la compra de un favorito usando transaction.atomic() y F().

    - Descuenta descuento_puntos del inventario del producto.
    - Marca el estado del favorito como 'comprado' (nuevo estado).
    - Si hay error de stock (F() < 0), hace rollback.
    - Patrón Post/Redirect/Get.
    """
    favorito = get_object_or_404(Favorito, pk=pk)
    producto = favorito.producto
    inventario = producto.inventario

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Actualizar inventario de forma atómica usando F()
                # Primero verificar que hay stock suficiente
                inventario_actual = Inventario.objects.filter(producto=producto).values_list('cantidad', flat=True).first()
                
                if inventario_actual is None or inventario_actual < favorito.descuento_puntos:
                    raise ValueError(
                        f"Stock insuficiente. Disponible: {inventario_actual or 0}, "
                        f"requerido: {favorito.descuento_puntos}"
                    )

                # Usar F() para actualizar de forma atómica (evita race conditions)
                rows_affected = Inventario.objects.filter(
                    producto=producto
                ).update(
                    cantidad=models.F('cantidad') - favorito.descuento_puntos
                )

                if rows_affected == 0:
                    raise ValueError("Error inesperado al actualizar inventario")

                # Marcar favorito como comprado
                favorito.estado = 'comprado'
                favorito.save(update_fields=['estado'])

                messages.success(
                    request,
                    f'Compra exitosa: "{producto.nombre}". '
                    f'Stock actual: {inventario.cantidad - favorito.descuento_puntos}'
                )

        except ValueError as e:
            # Rollback automático por transaction.atomic()
            messages.error(request, f'Error en la compra: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error inesperado: {str(e)}')

        return redirect('cliente_favoritos_list', pk=favorito.cliente.pk)

    return redirect('comprar_favorito_confirm', pk=pk)


def reporte_view(request):
    """Reporte global con aggregate() y annotate() aplicando floatformat:2.

    - Total global con aggregate() (Ejercicio 4).
    - Valores por objeto con annotate() (Ejercicio 5).
    - Agrupados por estado con values().annotate() (Ejercicio 5).
    - Agrupados por cliente con values().annotate() (Ejercicio 5).
    - Combinado estado × cliente con values().annotate() (Ejercicio 5).
    """
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

    # 3. Agrupados por estado con values().annotate()
    por_estado = Favorito.objects.values('estado').annotate(
        cantidad=Count('id'),
        descuento_total=Sum('descuento_puntos'),
        valor_total=Sum(F('descuento_puntos') * F('producto__precio'))
    )

    # 4. Agrupados por cliente con values().annotate()
    por_cliente = Favorito.objects.values('cliente__nombre').annotate(
        favoritos=Count('id'),
        descuento_total=Sum('descuento_puntos'),
        valor_total=Sum(F('descuento_puntos') * F('producto__precio'))
    ).order_by('-valor_total')

    # 5. Combinado estado × cliente con values().annotate()
    estado_cliente = Favorito.objects.values(
        'cliente__nombre', 'estado'
    ).annotate(
        descuento=Sum('descuento_puntos')
    ).order_by('cliente__nombre', 'estado')

    # Campos para labels de estado
    estado_choices = dict(Favorito._meta.get_field('estado').choices)

    context = {
        'global_res': global_res,
        'favoritos_annotated': favoritos_annotated,
        'por_estado': por_estado,
        'por_cliente': por_cliente,
        'estado_cliente': estado_cliente,
        'estado_choices': estado_choices,
    }
    return render(request, 'clientes/reporte.html', context)


# ═══════════════════════════════════════════════════════════
# Ejercicio 7: Views con QuerySet personalizado (as_manager)
# ═══════════════════════════════════════════════════════════

def favoritos_activos_view(request):
    """Listado de favoritos activos usando queryset personalizado.

    Usa: Favorito.objects.favoritos_activos()
    """
    favoritos = Favorito.objects.favoritos_activos().select_related(
        'cliente', 'producto'
    )
    return render(request, 'clientes/favoritos_activos.html', {
        'favoritos': favoritos,
    })


def favoritos_alto_valor_view(request, umbral=0):
    """Listado de favoritos con descuento_puntos > umbral usando queryset personalizado.

    Usa: Favorito.objects.con_valor_mayor_a(umbral)

    :param umbral: valor mínimo de descuento_puntos (default: 0, muestra todos)
    """
    try:
        umbral = int(umbral)
    except (TypeError, ValueError):
        umbral = 0

    favoritos = Favorito.objects.con_valor_mayor_a(umbral).select_related(
        'cliente', 'producto'
    )
    return render(request, 'clientes/favoritos_alto_valor.html', {
        'favoritos': favoritos,
        'umbral': umbral,
    })


# ═══════════════════════════════════════════════════════════
# Ejercicio 8: Medición de consultas y optimización N+1
# ═══════════════════════════════════════════════════════════

def optimizacion_nplus1_view(request):
    """Ejercicio 8: Mide el número de consultas y optimiza N+1.

    - Versión sin optimizar: lista todos los favoritos y accede a
      cliente.nombre y producto.nombre en el template (N+1 queries).
    - Versión optimizada: usa select_related('cliente', 'producto')
      para reducir a 1 consulta.
    - Usa connection.queries para contar las consultas SQL.
    """
    DEBUG = True  # connection.queries solo funciona con DEBUG = True

    # ── Versión sin optimizar (N+1) ──────────────────────────
    # Limpiar las consultas anteriores
    connection.queries_log.clear()

    favoritos_no_optimizados = Favorito.objects.all()
    # Acceder a las relaciones en Python (triggerá N+1)
    for fav in favoritos_no_optimizados:
        _ = fav.cliente.nombre
        _ = fav.producto.nombre

    queries_no_optimizadas = len(connection.queries)

    # ── Versión optimizada con select_related ─────────────────
    connection.queries_log.clear()

    favoritos_optimizados = Favorito.objects.select_related(
        'cliente', 'producto'
    ).all()
    # Ya no hace queries adicionales porque los FK están precargados
    for fav in favoritos_optimizados:
        _ = fav.cliente.nombre
        _ = fav.producto.nombre

    queries_optimizadas = len(connection.queries)

    context = {
        'favoritos_no_optimizados': Favorito.objects.all(),
        'favoritos_optimizados': favoritos_optimizados,
        'queries_no_optimizadas': queries_no_optimizadas,
        'queries_optimizadas': queries_optimizadas,
        'total_favoritos': Favorito.objects.count(),
    }
    return render(request, 'clientes/optimizacion_nplus1.html', context)


# ═══════════════════════════════════════════════════════════
# Ejercicio 10: Transaccional en la investigación propia
# ═══════════════════════════════════════════════════════════

def procesar_pedido_confirm(request, pk):
    """Ejercicio 10: Confirmación para procesar pago de un pedido.

    - Muestra un formulario de confirmación con los datos del pedido.
    - Usa transaction.atomic() y F() para aplicar la actualización atómica.
    """
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Crear un Pago vinculado al pedido con el mismo monto
                MetodoPago.objects.get(tipo='Tarjeta de Crédito')
                metodo = MetodoPago.objects.first()

                Pago = __import__('ventas.models', fromlist=['Pago']).Pago

                Pago.objects.create(
                    pedido=pedido,
                    metodo_pago=metodo,
                    monto=pedido.total,
                    estado='Procesado',
                )

                # Usar F() para actualizar el estado del pedido de forma atómica
                # Se usa F('total') para demostrar el uso de F() en una actualización
                rows = Pedido.objects.filter(pk=pedido.pk).update(
                    estado='Pagado',
                    total=F('total'),
                )

                if rows == 0:
                    raise RuntimeError("No se pudo actualizar el pedido")

                messages.success(
                    request,
                    f'Pedido {pedido.id_pedido} procesado exitosamente. '
                    f'Estado: Pagado.'
                )
                return redirect('cliente_list')

        except Exception as e:
            messages.error(request, f'Error al procesar el pedido: {str(e)}')
            return redirect('cliente_list')

    # GET: mostrar página de confirmación
    return render(request, 'clientes/procesar_pedido_confirm.html', {'pedido': pedido})


# ═══════════════════════════════════════════════════════════
# Ejercicio 11: View y Template de reportes con aggregate() y annotate()
# ═══════════════════════════════════════════════════════════

def reporte_ventas_view(request):
    """Ejercicio 11: Reporte de ventas con aggregate() y annotate().

    - aggregate(): total_pedidos (count), total_monto (sum), promedio_total (avg).
    - annotate() por estado con values('estado').annotate().
    - annotate() por cliente con values().annotate().
    - Templates con floatformat:2.
    """
    from ventas.models import Pago

    # 1. Resumen global con aggregate()
    global_res = Pedido.objects.aggregate(
        total_pedidos=Count('pk'),
        total_monto=Sum('total'),
        promedio_total=Avg('total'),
    )

    # 2. Desglose por estado con values().annotate()
    por_estado = Pedido.objects.values('estado').annotate(
        total_pedidos=Count('pk'),
        total_monto=Sum('total'),
        promedio_total=Avg('total'),
    ).order_by('-total_monto')

    # 3. Estadísticas por cliente con values().annotate()
    por_cliente = Pedido.objects.values(
        'cliente__nombre', 'cliente__apellido'
    ).annotate(
        total_pedidos=Count('pk'),
        total_monto=Sum('total'),
        promedio_total=Avg('total'),
    ).order_by('-total_monto')

    context = {
        'global_res': global_res,
        'por_estado': por_estado,
        'por_cliente': por_cliente,
    }
    return render(request, 'clientes/reporte_ventas.html', context)


# ═══════════════════════════════════════════════════════════
# Ejercicio 12: QuerySet personalizado en la investigación propia
# ═══════════════════════════════════════════════════════════

def pedidos_pendientes_view(request, umbral=0):
    """Ejercicio 12: Muestra pedidos usando QuerySet personalizado.

    Usa:
    - Pedido.objects.pedidos_pendientes() → filtra estado='Pendiente'
    - Pedido.objects.con_mayor_a(monto) → filtra total > monto

    :param umbral: monto mínimo para con_mayor_a (default: 0)
    """
    try:
        umbral = float(umbral)
    except (TypeError, ValueError):
        umbral = 0

    # Método 1: pedidos pendientes
    pendientes = Pedido.objects.pedidos_pendientes()

    # Método 2: pedidos con total mayor al umbral
    mayores = Pedido.objects.con_mayor_a(umbral)

    context = {
        'pendientes': pendientes,
        'mayores_a_umbral': mayores,
        'umbral': umbral,
    }
    return render(request, 'clientes/pedidos_pendientes.html', context)


# ═══════════════════════════════════════════════════════════
# Ejercicio 13: Medir y optimizar N+1 en la investigación propia
# ═══════════════════════════════════════════════════════════

def optimizacion_nplus1_pedidos_view(request):
    """Ejercicio 13: Medir y optimizar el problema N+1 en el listado de Pedidos.

    - Sin optimizar: recorre Pedido.objects.all() accediendo a cliente, detalles, producto.
    - Optimizado: usa select_related('cliente') y prefetch_related('detalles__producto').
    - Mide las consultas con connection.queries (DEBUG=True).
    """
    from ventas.models import Pedido, DetallePedido

    # 1. Sin optimización
    connection.queries_log.clear()

    pedidos_no_optimizados = list(Pedido.objects.all().select_related('cliente'))
    for pedido in pedidos_no_optimizados:
        _ = pedido.cliente.nombre
        _ = pedido.cliente.apellido
        for detalle in pedido.detalles.all():
            _ = detalle.producto.nombre
            _ = detalle.cantidad

    queries_no_optimizadas = len(connection.queries)
    queries_detail_no_opt = list(connection.queries)

    # 2. Con optimización (select_related + prefetch_related)
    connection.queries_log.clear()

    pedidos_optimizados = list(
        Pedido.objects.all()
        .select_related('cliente')
        .prefetch_related('detalles__producto')
    )
    for pedido in pedidos_optimizados:
        _ = pedido.cliente.nombre
        _ = pedido.cliente.apellido
        for detalle in pedido.detalles.all():
            _ = detalle.producto.nombre
            _ = detalle.cantidad

    queries_optimizadas = len(connection.queries)
    queries_detail_opt = list(connection.queries)

    context = {
        'pedidos_no_optimizados': pedidos_no_optimizados,
        'pedidos_optimizados': pedidos_optimizados,
        'queries_no_optimizadas': queries_no_optimizadas,
        'queries_optimizadas': queries_optimizadas,
        'queries_detail_no_opt': queries_detail_no_opt,
        'queries_detail_opt': queries_detail_opt,
    }
    return render(
        request,
        'clientes/optimizacion_nplus1_pedidos.html',
        context
    )
