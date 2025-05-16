from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Product, CartItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from myapp.models import Product
import random



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
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Nombre de usuario ya existe'}, status=400)
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return JsonResponse({'message': '¡Registro exitoso!'}, status=200)
    return render(request, 'home.html')


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


def perfil(request):
    return render(request, 'perfil.html')

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

def bajos(request):
    return render(request, 'bajos.html')

def teclados(request):
    return render(request, 'teclados.html')

def ofertas(request):
    all_products = list(Product.objects.all())
    displayed_products = random.sample(all_products, 4)  # Mostrar 4 productos aleatorios
    total_quantity = 0
    if request.user.is_authenticated:
        total_quantity = sum(item.quantity for item in CartItem.objects.filter(user=request.user))
    
    return render(request, 'ofertas.html', {'displayed_products': displayed_products, 'total_quantity': total_quantity})


def audio_y_grabacion(request):
    return render(request, 'audio_y_grabacion.html')

def microfonos(request):
    return render(request, 'microfonos.html')

def amplificadores(request):
    return render(request, 'amplificadores.html')

def pedales(request):
    return render(request, 'pedales.html')
