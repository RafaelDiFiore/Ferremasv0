from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('purchase/', views.purchase, name='purchase'),
    path('martillos/', views.martillos, name='martillos'),
    path('alicates/', views.alicates, name='alicates'),
    path('ofertas/', views.ofertas, name='ofertas'),
    path('administrador/', views.administrador, name='administrador'),
    path('cuenta/', views.cuenta_usuario, name='cuenta'),
    path('panel-admin/productos/', views.admin_productos_view, name='productos_admin'),
    path('panel-admin/productos/nuevo/', views.crear_producto, name='producto_nuevo'),
    path('panel-admin/productos/editar/<int:producto_id>/', views.editar_producto, name='producto_editar'),
    path('panel-admin/productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='producto_eliminar'),
    path('panel/perfiles/crear/', views.crear_perfil_manual, name='crear_perfil'),
    path('panel/perfiles/editar/<int:pk>/', views.editar_perfil_manual, name='editar_perfil'),
    path('panel/perfiles/eliminar/<int:pk>/', views.eliminar_perfil, name='eliminar_perfil'),
    path('bodeguero/', views.vista_bodeguero, name='vista_bodeguero'),
    path('cliente/', views.vista_cliente, name='vista_cliente'),
    path('cliente/editar/', views.editar_perfil_cliente, name='editar_perfil_cliente'),




    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)