from django.shortcuts import render, redirect, get_object_or_404

from .models import CartProducts, Product  # Importa los modelos necesarios.
from .utils import get_or_create_cart  # Función utilitaria para obtener o crear un carrito.

# Vista para mostrar el contenido del carrito.
def cart(request):
    # Obtiene o crea un carrito asociado al usuario actual o a la sesión.
    cart = get_or_create_cart(request)

    # Renderiza la plantilla 'cart.html' con el carrito en el contexto.
    return render(request, 'carts/cart.html', {
        'cart': cart
    })

# Vista para añadir productos al carrito.
def add(request):
    # Obtiene o crea un carrito para el usuario o la sesión.
    cart = get_or_create_cart(request)
    
    # Obtiene el producto a partir del ID proporcionado en el POST. Si no existe, retorna un error 404.
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    
    # Obtiene la cantidad especificada en el POST o 1 por defecto.
    quantity = int(request.POST.get('quantity', 1))

    '''
    Código comentado que utiliza una relación directa muchos a muchos para agregar el producto al carrito.
    cart.products.add(product, through_defaults={
        'quantity' : quantity
    })
    '''

    # Utiliza el manager personalizado de `CartProducts` para crear o actualizar la cantidad del producto en el carrito.
    cart_product = CartProducts.objects.create_or_update_quantity(
        cart=cart,
        product=product,
        quantity=quantity
    )

    # Renderiza la plantilla 'add.html' con los detalles del producto añadido al carrito.
    return render(request, 'carts/add.html', {
        'quantity': quantity,
        'cart_product': cart_product,
        'product': product
    })

# Vista para eliminar un producto del carrito.
def remove(request):
    # Obtiene o crea un carrito para el usuario o la sesión.
    cart = get_or_create_cart(request)
    
    # Obtiene el producto a partir del ID proporcionado en el POST. Si no existe, retorna un error 404.
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))

    # Elimina el producto del carrito.
    cart.products.remove(product)

    # Redirige a la vista del carrito para mostrar los productos restantes.
    return redirect('carts:cart')
