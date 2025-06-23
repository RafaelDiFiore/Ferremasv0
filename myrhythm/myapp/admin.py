from django.contrib import admin
from .models import Product
from .models import Perfil

admin.site.register(Product)

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo')
    list_filter = ('tipo',)