from django.shortcuts import render, redirect  # Importa funciones para renderizar y redirigir
from django.contrib.auth import logout  # Importa la función para cerrar sesión
from django.contrib import messages  # Importa el sistema de mensajes de Django
from django.contrib.auth import authenticate, login  # Importa funciones para autenticar e iniciar sesión
from django.http import HttpResponseRedirect  # Importa la función para redirigir respuestas

from users.models import User  # Importa el modelo User desde la aplicación 'users'
from .forms import RegisterForm  # Importa el formulario de registro
from products.models import Product  # Importa el modelo Product desde la aplicación 'products'

def index(request):
    """
    Vista de la página principal que muestra la lista de productos.
    """
    products = Product.objects.all().order_by('id')  # Obtiene todos los productos y los ordena por id

    return render(request, 'index.HTML', {
        'message': 'hola mundo desde la vista',  # Mensaje a mostrar en la plantilla
        'title': 'Titulo',  # Título de la página
        'products': products,  # Lista de productos a mostrar
    })          

def login_views(request):
    """
    Vista para el inicio de sesión de usuarios.
    Redirige a la página principal si el usuario ya está autenticado.
    """
    if request.user.is_authenticated:
        return redirect('index')  # Redirige a la página principal si ya está autenticado
    
    if request.method == 'POST':
        username = request.POST.get('username')  # Obtiene el nombre de usuario del formulario
        password = request.POST.get('password')  # Obtiene la contraseña del formulario

        user = authenticate(username=username, password=password)  # Intenta autenticar al usuario
        if user:
            login(request, user)  # Inicia sesión si la autenticación es exitosa
            messages.success(request, 'Bienvenido {}'.format(user.username))  # Mensaje de éxito

            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])  # Redirige a la URL especificada
            return redirect('index')  # Redirige a la página principal
        else:
            messages.error(request, "Usuarios o contrasena no validos")  # Mensaje de error si la autenticación falla

    return render(request, 'users/login.HTML')  # Renderiza la plantilla de inicio de sesión

def logout_views(request):
    """
    Vista para cerrar la sesión de un usuario.
    Muestra un mensaje de éxito y redirige a la página de inicio de sesión.
    """
    logout(request)  # Cierra la sesión
    messages.success(request, 'Session cerrada exitosamente')  # Mensaje de éxito
    return redirect('login')  # Redirige a la página de inicio de sesión

def register(request):
    """
    Vista para registrar nuevos usuarios.
    Redirige a la página principal si el usuario ya está autenticado.
    """
    form = RegisterForm(request.POST or None)  # Crea el formulario, con datos POST si están disponibles
    if request.user.is_authenticated:
        return redirect('contactos')  # Redirige a la página principal si ya está autenticado
    
    if request.method == 'POST' and form.is_valid():
        user = form.save()  # Crea un nuevo usuario si el formulario es válido
        if user:
            messages.success(request, 'Usuario creado exitosamente')  # Mensaje de éxito
            return redirect('contacto')  # Redirige a la página principal

    return render(request, 'users/register.html', {
        'form': form  # Renderiza la plantilla de registro con el formulario
    })
