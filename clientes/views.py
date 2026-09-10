from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, MetodoPago, Carrito, Direccion, Resena, PerfilCliente, Favorito
from .forms import FavoritoForm

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
        form = FavoritoForm()
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