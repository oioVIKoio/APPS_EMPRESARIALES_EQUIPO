from django.shortcuts import render, redirect
from .models import Pedido, DetallePedido, Pago, Envio, Cupon
from clientes.models import Cliente, MetodoPago, Direccion
from catalogo.models import Producto


# ---------------------------------------------------------------------------
# Inicio
# ---------------------------------------------------------------------------
def inicio(request):
    return render(request, 'ventas/inicio.html')


# ---------------------------------------------------------------------------
# Pedido
# ---------------------------------------------------------------------------
def lista_pedidos(request):
    pedidos = (Pedido.objects.select_related('cliente', 'pago__metodo_pago', 'envio')
               .prefetch_related('detalles__producto').order_by('-fecha_pedido'))

    return render(
        request,
        'ventas/pedidos/lista.html',
        {'pedidos': pedidos}
    )


def crear_pedido(request):
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        Pedido.objects.create(
            cliente_id=request.POST['cliente'],
            estado=request.POST['estado'],
            total=request.POST['total'],
        )

        return redirect('ventas:lista_pedidos')

    return render(
        request,
        'ventas/pedidos/crear.html',
        {'clientes': clientes}
    )


def editar_pedido(request, id):
    pedido = Pedido.objects.get(id_pedido=id)
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        pedido.cliente_id = request.POST['cliente']
        pedido.estado = request.POST['estado']
        pedido.total = request.POST['total']

        pedido.save()

        return redirect('ventas:lista_pedidos')

    return render(
        request,
        'ventas/pedidos/editar.html',
        {
            'pedido': pedido,
            'clientes': clientes,
            'opciones_estado': ['Pendiente', 'Confirmado', 'Enviado', 'Entregado', 'Cancelado'],
        }
    )


def eliminar_pedido(request, id):
    pedido = Pedido.objects.get(id_pedido=id)

    if request.method == 'POST':
        pedido.delete()

        return redirect('ventas:lista_pedidos')

    return render(
        request,
        'ventas/pedidos/eliminar.html',
        {'pedido': pedido}
    )


# ---------------------------------------------------------------------------
# DetallePedido
# ---------------------------------------------------------------------------
def lista_detalles(request):
    detalles = DetallePedido.objects.select_related('pedido__cliente', 'producto')

    return render(
        request,
        'ventas/detalles/lista.html',
        {'detalles': detalles}
    )


def crear_detalle(request):
    pedidos = Pedido.objects.all()
    productos = Producto.objects.all()

    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
        precio_unitario = request.POST['precio_unitario']

        DetallePedido.objects.create(
            pedido_id=request.POST['pedido'],
            producto_id=request.POST['producto'],
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=round(float(precio_unitario) * cantidad, 2),
        )

        return redirect('ventas:lista_detalles')

    return render(
        request,
        'ventas/detalles/crear.html',
        {
            'pedidos': pedidos,
            'productos': productos,
        }
    )


def editar_detalle(request, id):
    detalle = DetallePedido.objects.get(id_detalle=id)
    pedidos = Pedido.objects.all()
    productos = Producto.objects.all()

    if request.method == 'POST':
        cantidad = int(request.POST['cantidad'])
        precio_unitario = request.POST['precio_unitario']

        detalle.pedido_id = request.POST['pedido']
        detalle.producto_id = request.POST['producto']
        detalle.cantidad = cantidad
        detalle.precio_unitario = precio_unitario
        detalle.subtotal = round(float(precio_unitario) * cantidad, 2)

        detalle.save()

        return redirect('ventas:lista_detalles')

    return render(
        request,
        'ventas/detalles/editar.html',
        {
            'detalle': detalle,
            'pedidos': pedidos,
            'productos': productos,
        }
    )


def eliminar_detalle(request, id):
    detalle = DetallePedido.objects.get(id_detalle=id)

    if request.method == 'POST':
        detalle.delete()

        return redirect('ventas:lista_detalles')

    return render(
        request,
        'ventas/detalles/eliminar.html',
        {'detalle': detalle}
    )


# ---------------------------------------------------------------------------
# Pago
# ---------------------------------------------------------------------------
def lista_pagos(request):
    pagos = Pago.objects.select_related('pedido__cliente', 'metodo_pago')

    return render(
        request,
        'ventas/pagos/lista.html',
        {'pagos': pagos}
    )


def crear_pago(request):
    pedidos = Pedido.objects.all()
    metodos_pago = MetodoPago.objects.all()

    if request.method == 'POST':
        Pago.objects.create(
            pedido_id=request.POST['pedido'],
            metodo_pago_id=request.POST['metodo_pago'],
            monto=request.POST['monto'],
            estado=request.POST['estado'],
        )

        return redirect('ventas:lista_pagos')

    return render(
        request,
        'ventas/pagos/crear.html',
        {
            'pedidos': pedidos,
            'metodos_pago': metodos_pago,
        }
    )


def editar_pago(request, id):
    pago = Pago.objects.get(id_pago=id)
    pedidos = Pedido.objects.all()
    metodos_pago = MetodoPago.objects.all()

    if request.method == 'POST':
        pago.pedido_id = request.POST['pedido']
        pago.metodo_pago_id = request.POST['metodo_pago']
        pago.monto = request.POST['monto']
        pago.estado = request.POST['estado']

        pago.save()

        return redirect('ventas:lista_pagos')

    return render(
        request,
        'ventas/pagos/editar.html',
        {
            'pago': pago,
            'pedidos': pedidos,
            'metodos_pago': metodos_pago,
            'opciones_estado': ['Pendiente', 'Completado', 'Rechazado'],
        }
    )


def eliminar_pago(request, id):
    pago = Pago.objects.get(id_pago=id)

    if request.method == 'POST':
        pago.delete()

        return redirect('ventas:lista_pagos')

    return render(
        request,
        'ventas/pagos/eliminar.html',
        {'pago': pago}
    )


# ---------------------------------------------------------------------------
# Envio
# ---------------------------------------------------------------------------
def lista_envios(request):
    envios = Envio.objects.select_related('pedido__cliente', 'direccion__cliente')

    return render(
        request,
        'ventas/envios/lista.html',
        {'envios': envios}
    )


def crear_envio(request):
    pedidos = Pedido.objects.all()
    direcciones = Direccion.objects.all()

    if request.method == 'POST':
        Envio.objects.create(
            pedido_id=request.POST['pedido'],
            direccion_id=request.POST['direccion'],
            empresa_envio=request.POST['empresa_envio'],
            estado=request.POST['estado'],
        )

        return redirect('ventas:lista_envios')

    return render(
        request,
        'ventas/envios/crear.html',
        {
            'pedidos': pedidos,
            'direcciones': direcciones,
        }
    )


def editar_envio(request, id):
    envio = Envio.objects.get(id_envio=id)
    pedidos = Pedido.objects.all()
    direcciones = Direccion.objects.all()

    if request.method == 'POST':
        envio.pedido_id = request.POST['pedido']
        envio.direccion_id = request.POST['direccion']
        envio.empresa_envio = request.POST['empresa_envio']
        envio.estado = request.POST['estado']

        envio.save()

        return redirect('ventas:lista_envios')

    return render(
        request,
        'ventas/envios/editar.html',
        {
            'envio': envio,
            'pedidos': pedidos,
            'direcciones': direcciones,
            'opciones_estado': ['Pendiente', 'En tránsito', 'Entregado', 'Devuelto'],
        }
    )


def eliminar_envio(request, id):
    envio = Envio.objects.get(id_envio=id)

    if request.method == 'POST':
        envio.delete()

        return redirect('ventas:lista_envios')

    return render(
        request,
        'ventas/envios/eliminar.html',
        {'envio': envio}
    )


# ---------------------------------------------------------------------------
# Cupon
# ---------------------------------------------------------------------------
def lista_cupones(request):
    cupones = Cupon.objects.order_by('-activo', 'codigo')

    return render(
        request,
        'ventas/cupones/lista.html',
        {'cupones': cupones}
    )


def crear_cupon(request):
    if request.method == 'POST':
        Cupon.objects.create(
            codigo=request.POST['codigo'],
            descripcion=request.POST['descripcion'],
            descuento=request.POST['descuento'],
            fecha_inicio=request.POST['fecha_inicio'],
            fecha_fin=request.POST['fecha_fin'],
            activo=request.POST.get('activo') == 'on',
        )

        return redirect('ventas:lista_cupones')

    return render(
        request,
        'ventas/cupones/crear.html'
    )


def editar_cupon(request, id):
    cupon = Cupon.objects.get(id_cupon=id)

    if request.method == 'POST':
        cupon.codigo = request.POST['codigo']
        cupon.descripcion = request.POST['descripcion']
        cupon.descuento = request.POST['descuento']
        cupon.fecha_inicio = request.POST['fecha_inicio']
        cupon.fecha_fin = request.POST['fecha_fin']
        cupon.activo = request.POST.get('activo') == 'on'

        cupon.save()

        return redirect('ventas:lista_cupones')

    return render(
        request,
        'ventas/cupones/editar.html',
        {'cupon': cupon}
    )


def eliminar_cupon(request, id):
    cupon = Cupon.objects.get(id_cupon=id)

    if request.method == 'POST':
        cupon.delete()

        return redirect('ventas:lista_cupones')

    return render(
        request,
        'ventas/cupones/eliminar.html',
        {'cupon': cupon}
    )
