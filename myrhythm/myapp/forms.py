from django import forms
from .models import Product
from .models import Perfil
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image', 'categoria']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['user', 'tipo']