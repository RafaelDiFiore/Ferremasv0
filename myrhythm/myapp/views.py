from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Product
from django.contrib import messages
from django.urls import reverse
from myapp.models import Product
import random
from django.contrib.auth.decorators import login_required
from .models import Perfil, CartItem, Compra
from .forms import PerfilForm, ProductForm

# from transbank.webpay.webpay_plus.transaction import Transaction
# from transbank.common.integration_type import IntegrationType
# from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt

# Transaction.commerce_code = '597055555532'
# Transaction.api_key = 'X'
# Transaction.integration_type = IntegrationType.TEST

# tx = Transaction()  # sin argumentos



def home(request):
    all_products = list(Product.objects.all())
    displayed_products = random.sample(all_products, 4)
    total_quantity = 0
    if request.user.is_authenticated:
        total_quantity = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
    
    return render(request, 'home.html', {'displayed_products': displayed_products, 'total_quantity': total_quantity})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': '¡Login exitoso!'}, status=200)
        else:
            return JsonResponse({'message': 'Usuario o contraseña incorrectos'}, status=400)
    return render(request, 'home.html')


def register_view(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        rut = request.POST['rut']
        email = request.POST['email']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        password = request.POST['password']

        username = email.split('@')[0]
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Nombre de usuario ya existe'}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = nombre
        user.save()

        Perfil.objects.create(
            user=user,
            tipo='cliente',
            rut=rut,
            direccion=direccion,
            telefono=telefono
        )

        return JsonResponse({'message': '¡Registro exitoso!'}, status=200)

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()

        return JsonResponse({'message': 'Producto añadido al carrito'})



@login_required(login_url='home')
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_quantity = sum(item.quantity for item in cart_items)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'view_cart.html', {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price
    })


@login_required
def update_cart(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        action = request.POST.get('action')
        
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
            else:
                cart_item.delete()
                return JsonResponse({'message': 'Producto eliminado del carrito'})

        cart_item.save()
        return JsonResponse({'message': 'Carrito actualizado'})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def purchase(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        cart_items.delete()
        messages.success(request, 'Compra realizada con éxito.')
        return JsonResponse({'message': 'Compra realizada con éxito.', 'redirect_url': reverse('home')})
    return redirect('view_cart')


@login_required
def cuenta_usuario(request):
    total_quantity = 0
    if request.user.is_authenticated:
        total_quantity = sum(item.quantity for item in CartItem.objects.filter(user=request.user))

    return render(request, 'cuenta.html', {'total_quantity': total_quantity})

def martillos(request):
    martillos = Product.objects.filter(categoria__iexact='Martillo')
    total_quantity = 0
    if request.user.is_authenticated:
        total_quantity = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
    
    return render(request, 'martillos.html', {'martillos': martillos, 'total_quantity': total_quantity})


def alicates(request):
    alicatess = Product.objects.filter(categoria__iexact='Alicate')
    total_quantity = 0
    if request.user.is_authenticated:
        total_quantity = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
    
    return render(request, 'alicates.html', {'alicatess': alicatess, 'total_quantity': total_quantity})

def ofertas(request):
    all_products = list(Product.objects.all())
    displayed_products = random.sample(all_products, 4)  # Mostrar 4 productos aleatorios
    total_quantity = 0
    if request.user.is_authenticated:
        total_quantity = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
    
    return render(request, 'ofertas.html', {'displayed_products': displayed_products, 'total_quantity': total_quantity})

#CUENTAS DE USUARIO

@login_required(login_url='login')
def cuenta_usuario(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user, defaults={'tipo': 'cliente'})
    total_quantity = sum(item.quantity for item in CartItem.objects.filter(user=request.user))

    if perfil.tipo == 'administrador':
        return redirect('administrador')
    elif perfil.tipo == 'contador':
        return redirect('contador')
    elif perfil.tipo == 'bodeguero':
        return redirect('vista_bodeguero')
    elif perfil.tipo == 'vendedor':
        return redirect('vendedor')
    elif perfil.tipo == 'cliente':
        return redirect('vista_cliente')

    return render(request, 'perfil.html', {'total_quantity': total_quantity})

@login_required
def administrador(request):
    perfiles = Perfil.objects.select_related('user').all()
    return render(request, 'administrador.html', {'perfiles': perfiles})

def cerrar_sesion(request):
    logout(request)
    return redirect('login')  # o 'home', o 'cuenta'



#CRUD PRODUCTOS

def admin_productos_view(request):
    productos = Product.objects.all()
    return render(request, 'productos_admin.html', {'productos': productos})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect('productos_admin')
    else:
        form = ProductForm()
    return render(request, 'producto_form.html', {'form': form, 'accion': 'Crear'})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Product, pk=producto_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('vista_bodeguero')  # si estás editando desde bodeguero
    else:
        form = ProductForm(instance=producto)

    return render(request, 'producto_formulario (1).html', {
        'form': form,
        'accion': 'Editar'
    })


@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Product, pk=producto_id)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente.")
    return redirect('productos_admin')

def lista_perfiles(request):
    perfiles = Perfil.objects.select_related('user').all()
    return render(request, 'perfiles_admin.html', {'perfiles': perfiles})



#CRUD PERFILES-USUARIOS

def eliminar_perfil(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    perfil.delete()
    return redirect('lista_perfiles')

def crear_perfil_manual(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        correo = request.POST.get('correo', '').strip()
        tipo = request.POST.get('tipo')

        if not nombre or not correo or not tipo:
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'perfil_form.html')

        if User.objects.filter(email=correo).exists():
            messages.error(request, "Ya existe un usuario con ese correo.")
            return render(request, 'perfil_form.html')

        base_username = correo.split('@')[0]
        username = base_username
        count = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{count}"
            count += 1

        if " " in nombre:
            partes = nombre.split()
            first_name = partes[0]
            last_name = " ".join(partes[1:])
        else:
            first_name = nombre
            last_name = ""

        user = User.objects.create_user(username=username, email=correo)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        perfil = Perfil(user=user, tipo=tipo)
        perfil.save()

        messages.success(request, "Usuario creado exitosamente.")
        return redirect('administrador')

    return render(request, 'perfil_form.html')

def editar_perfil_manual(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    user = perfil.user

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        correo = request.POST.get('correo', '').strip()
        tipo = request.POST.get('tipo')

        if not nombre or not correo or not tipo:
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'perfil_form.html')

        # Actualizar nombre completo
        if " " in nombre:
            partes = nombre.split()
            user.first_name = partes[0]
            user.last_name = " ".join(partes[1:])
        else:
            user.first_name = nombre
            user.last_name = ""

        user.email = correo
        user.save()

        perfil.tipo = tipo
        perfil.save()

        messages.success(request, "Perfil actualizado correctamente.")
        return redirect('administrador')

    nombre_actual = f"{user.first_name} {user.last_name}".strip()
    return render(request, 'perfil_form.html', {
        'nombre': nombre_actual,
        'correo': user.email,
        'tipo': perfil.tipo,
    })

#VISTA BODEGUERO

@login_required
def vista_bodeguero(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo != 'bodeguero':
        return redirect('administrador')  # redirige si no es bodeguero

    productos = Product.objects.all()
    return render(request, 'bodeguero_productos.html', {'productos': productos})


#VISTA DEL CLIENTE - PERFIL BASICO

@login_required
def vista_cliente(request):
    perfil = request.user.perfil

    if perfil.tipo != 'cliente':
        return redirect('perfil')  # o redirige a otra vista segura

    compras = Compra.objects.filter(user=request.user).order_by('-fecha')

    return render(request, 'cliente_panel.html', {
        'profile': perfil,
        'compras': compras,
    })

@login_required
def editar_perfil_cliente(request):
    perfil = request.user.perfil

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono')

        request.user.first_name = nombre
        request.user.save()

        perfil.direccion = direccion
        perfil.telefono = telefono
        perfil.save()

        return redirect('vista_cliente')

    return render(request, 'editar_perfil_cliente.html', {
        'nombre': request.user.first_name,
        'direccion': perfil.direccion,
        'telefono': perfil.telefono,
    })

# tx = Transaction(
#     commerce_code='597055555532',
#     api_key='X',
#     integration_type=IntegrationType.TEST
# )


# # CREA LA TRANSACCIÓN
# def purchase(request):
#     if request.method == 'POST':
#         cart_items = CartItem.objects.filter(user=request.user)
#         total_price = sum(item.product.price * item.quantity for item in cart_items)

#         # Crear transacción de prueba
#         response = tx.create(
#             buy_order=f"ORDER-{request.user.id}-{cart_items.first().id if cart_items else '000'}",
#             session_id=str(request.user.id),
#             amount=total_price,
#             return_url=request.build_absolute_uri('/webpay/commit/')
#         )

#         url = response['url']
#         token = response['token']

#         # Redirige al formulario de pago de Transbank
#         return render(request, 'redirect_to_webpay.html', {'url': url, 'token': token})