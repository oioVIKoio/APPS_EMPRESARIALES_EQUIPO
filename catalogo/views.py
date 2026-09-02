from django.shortcuts import render, redirect
from .models import Categoria, Marca, Proveedor, Producto, Inventario


def inicio(request):
    productos = Producto.objects.all()

    return render(
        request,
        'catalogo/inicio.html',
        {'productos': productos}
    )

def lista_productos(request):
    productos = Producto.objects.all()
    return render(
        request,
        'catalogo/productos/lista.html',
        {'productos': productos}
    )


def crear_producto(request):
    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        Producto.objects.create(
            nombre=request.POST['nombre'],
            descripcion=request.POST['descripcion'],
            precio=request.POST['precio'],
            categoria_id=request.POST['categoria'],
            marca_id=request.POST['marca'],
            proveedor_id=request.POST['proveedor'],
        )

        return redirect('catalogo:lista_productos')

    return render(
        request,
        'catalogo/productos/crear.html',
        {
            'categorias': categorias,
            'marcas': marcas,
            'proveedores': proveedores,
        }
    )

def editar_producto(request, id):
    producto = Producto.objects.get(id=id)

    categorias = Categoria.objects.all()
    marcas = Marca.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        producto.nombre = request.POST['nombre']
        producto.descripcion = request.POST['descripcion']
        producto.precio = request.POST['precio']
        producto.categoria_id = request.POST['categoria']
        producto.marca_id = request.POST['marca']
        producto.proveedor_id = request.POST['proveedor']

        producto.save()

        return redirect('catalogo:lista_productos')

    return render(
        request,
        'catalogo/productos/editar.html',
        {
            'producto': producto,
            'categorias': categorias,
            'marcas': marcas,
            'proveedores': proveedores,
        }
    )

def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)

    if request.method == 'POST':
        producto.delete()

        return redirect('catalogo:lista_productos')

    return render(
        request,
        'catalogo/productos/eliminar.html',
        {'producto': producto}
    )
def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(
        request,
        'catalogo/categorias/lista.html',
        {'categorias': categorias}
    )
def crear_categoria(request):
    if request.method == 'POST':
        Categoria.objects.create(
            nombre=request.POST['nombre'],
            descripcion=request.POST['descripcion']
        )

        return redirect('catalogo:lista_categorias')

    return render(
        request,
        'catalogo/categorias/crear.html'
    )


def editar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)

    if request.method == 'POST':
        categoria.nombre = request.POST['nombre']
        categoria.descripcion = request.POST['descripcion']

        categoria.save()

        return redirect('catalogo:lista_categorias')

    return render(
        request,
        'catalogo/categorias/editar.html',
        {'categoria': categoria}
    )


def eliminar_categoria(request, id):
    categoria = Categoria.objects.get(id=id)

    if request.method == 'POST':
        categoria.delete()

        return redirect('catalogo:lista_categorias')

    return render(
        request,
        'catalogo/categorias/eliminar.html',
        {'categoria': categoria}
    )


def lista_marcas(request):
    marcas = Marca.objects.all()
    return render(
        request,
        'catalogo/marcas/lista.html',
        {'marcas': marcas}
    )
def crear_marca(request):
    if request.method == 'POST':
        Marca.objects.create(
            nombre=request.POST['nombre'],
            descripcion=request.POST['descripcion']
        )

        return redirect('catalogo:lista_marcas')

    return render(
        request,
        'catalogo/marcas/crear.html'
    )


def editar_marca(request, id):
    marca = Marca.objects.get(id=id)

    if request.method == 'POST':
        marca.nombre = request.POST['nombre']
        marca.descripcion = request.POST['descripcion']

        marca.save()

        return redirect('catalogo:lista_marcas')

    return render(
        request,
        'catalogo/marcas/editar.html',
        {'marca': marca}
    )


def eliminar_marca(request, id):
    marca = Marca.objects.get(id=id)

    if request.method == 'POST':
        marca.delete()

        return redirect('catalogo:lista_marcas')

    return render(
        request,
        'catalogo/marcas/eliminar.html',
        {'marca': marca}
    )

def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(
        request,
        'catalogo/proveedores/lista.html',
        {'proveedores': proveedores}
    )
def crear_proveedor(request):
    if request.method == 'POST':
        Proveedor.objects.create(
            nombre=request.POST['nombre'],
            telefono=request.POST['telefono'],
            email=request.POST['email']
        )

        return redirect('catalogo:lista_proveedores')

    return render(
        request,
        'catalogo/proveedores/crear.html'
    )


def editar_proveedor(request, id):
    proveedor = Proveedor.objects.get(id=id)

    if request.method == 'POST':
        proveedor.nombre = request.POST['nombre']
        proveedor.telefono = request.POST['telefono']
        proveedor.email = request.POST['email']

        proveedor.save()

        return redirect('catalogo:lista_proveedores')

    return render(
        request,
        'catalogo/proveedores/editar.html',
        {'proveedor': proveedor}
    )


def eliminar_proveedor(request, id):
    proveedor = Proveedor.objects.get(id=id)

    if request.method == 'POST':
        proveedor.delete()

        return redirect('catalogo:lista_proveedores')

    return render(
        request,
        'catalogo/proveedores/eliminar.html',
        {'proveedor': proveedor}
    )

def lista_inventarios(request):
    inventarios = Inventario.objects.all()
    return render(
        request,
        'catalogo/inventario/lista.html',
        {'inventarios': inventarios}
    )

def crear_inventario(request):
    productos = Producto.objects.all()

    if request.method == 'POST':
        Inventario.objects.create(
            producto_id=request.POST['producto'],
            cantidad=request.POST['cantidad'],
            stock_minimo=request.POST['stock_minimo']
        )

        return redirect('catalogo:lista_inventarios')

    return render(
        request,
        'catalogo/inventario/crear.html',
        {'productos': productos}
    )


def editar_inventario(request, id):
    inventario = Inventario.objects.get(id=id)
    productos = Producto.objects.all()

    if request.method == 'POST':
        inventario.producto_id = request.POST['producto']
        inventario.cantidad = request.POST['cantidad']
        inventario.stock_minimo = request.POST['stock_minimo']

        inventario.save()

        return redirect('catalogo:lista_inventarios')

    return render(
        request,
        'catalogo/inventario/editar.html',
        {
            'inventario': inventario,
            'productos': productos,
        }
    )


def eliminar_inventario(request, id):
    inventario = Inventario.objects.get(id=id)

    if request.method == 'POST':
        inventario.delete()

        return redirect('catalogo:lista_inventarios')

    return render(
        request,
        'catalogo/inventario/eliminar.html',
        {'inventario': inventario}
    )