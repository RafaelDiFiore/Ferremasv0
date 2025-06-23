# myapp/models.py
from django.contrib.auth.models import User
from django.db import models

class Perfil(models.Model):
    TIPOS_USUARIO = [
        ('administrador', 'Administrador'),
        ('contador', 'Contador'),
        ('bodeguero', 'Bodeguero'),
        ('vendedor', 'Vendedor'),
        ('cliente', 'Cliente'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='cliente')
    rut = models.CharField(max_length=9, default='Sin RUT')
    direccion = models.CharField(max_length=255, default='Sin dirección')
    telefono = models.CharField(max_length=15, default='Sin Telefono' )


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    categoria = models.CharField(max_length=50, default="General")  # 🔧 este campo

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

class Compra(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.CharField(max_length=255)  # o ForeignKey a tu modelo Producto
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.producto}"