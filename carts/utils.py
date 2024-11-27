from .models import Cart

# Función para obtener o crear un carrito de compras.
def get_or_create_cart(request):
    # Si el usuario está autenticado, lo asigna a la variable user. Si no, asigna None.
    user = request.user if request.user.is_authenticated else None
    
    # Obtiene el 'cart_id' de la sesión actual del usuario.
    cart_id = request.session.get('cart_id')

    # Busca en la base de datos el carrito que coincida con el 'cart_id'.
    cart = Cart.objects.filter(cart_id=cart_id).first()
    
    # Si no existe ningún carrito con ese 'cart_id' y hay una petición, crea uno nuevo.
    if cart is None and request:
        cart = Cart.objects.create(user=user)

    # Si el usuario está autenticado y el carrito aún no tiene usuario asignado, lo asigna.
    if user and cart.user is None:
        cart.user = user
        cart.save()

    # Guarda el 'cart_id' del carrito actual en la sesión del usuario.
    request.session['cart_id'] = cart.cart_id

    # Retorna el carrito, ya sea existente o recién creado.
    return cart

# Función para destruir (o borrar) el carrito de la sesión.
def destroy_cart(request):
    # Elimina el 'cart_id' de la sesión, efectivamente "destruyendo" el carrito.
    request.session["cart_id"] = None
