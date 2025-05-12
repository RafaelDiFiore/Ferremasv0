from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('purchase/', views.purchase, name='purchase'),
    path('guitarras/', views.guitarras, name='guitarras'),
    path('baterias/', views.baterias, name='baterias'),
    path('bajos/', views.bajos, name='bajos'),
    path('teclados/', views.teclados, name='teclados'),
    path('audio_y_grabacion/', views.audio_y_grabacion, name='audio_y_grabacion'),
    path('microfonos/', views.microfonos, name='microfonos'),
    path('amplificadores/', views.amplificadores, name='amplificadores'),
    path('pedales/', views.pedales, name='pedales'),
    path('ofertas/', views.ofertas, name='ofertas'),

   
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)