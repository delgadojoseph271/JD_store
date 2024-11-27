"""
URL configuration for JD_store project.

El `urlpatterns` lista las rutas de URL a vistas. Para más información, consulta:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""

from django.contrib import admin  # Importa el módulo de administración de Django
from django.urls import path, include  # Importa funciones para definir rutas
from django.conf.urls.static import static  # Permite servir archivos estáticos
from django.conf import settings  # Configuraciones del proyecto

from . import views  # Importa las vistas definidas en el módulo actual
from products.views import ProductListView  # Importa la vista de lista de productos

urlpatterns = [
    # Ruta para la página principal que muestra la lista de productos
    path('', ProductListView.as_view(), name='index'),  
    
    # Rutas para la gestión de usuarios
    path('usuarios/login', views.login_views, name='login'),  # Vista de inicio de sesión
    path('usuarios/logout', views.logout_views, name='logout'),  # Vista para cerrar sesión
    path('usuarios/registros', views.register, name='register'),  # Vista de registro de usuarios
    
    # Ruta para el panel de administración
    path('admin/', admin.site.urls),  
    
    # Inclusión de URLs de aplicaciones específicas
    path('productos/', include('products.urls')),  # Rutas relacionadas con productos
    path('carrito/', include('carts.urls')),  # Rutas relacionadas con el carrito de compras
    path('orden/', include('orders.urls')),  # Rutas relacionadas con órdenes
    path('direcciones/', include('shipping_addresses.urls')),  # Rutas para direcciones de envío
    path('codigos/', include('promo_codes.urls')),  # Rutas para códigos promocionales
    path('pagos/', include('billing_profiles.urls')),  # Rutas para perfiles de pago
]

# Configuración para servir archivos multimedia en modo de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
