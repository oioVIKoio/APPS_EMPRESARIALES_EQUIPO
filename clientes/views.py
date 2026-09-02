from django.shortcuts import render, redirect
from .models import Cliente, MetodoPago, Carrito, Direccion, Resena


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
    direcciones = Direccion.objects.all()
    return render(request, 'clientes/direccion_list.html', {'direcciones': direcciones})


def resena_list(request):
    resenas = Resena.objects.all()
    return render(request, 'clientes/resena_list.html', {'resenas': resenas})

