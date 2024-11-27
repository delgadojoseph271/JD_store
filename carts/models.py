import uuid
import decimal

from django.db import models

from users.models import User  # Importa el modelo de usuario.
from products.models import Product  # Importa el modelo de producto.

from orders.common import OrderStatus  # Importa los estados posibles de una orden (completada, creada, etc.).

from django.db.models.signals import post_save, pre_save, m2m_changed  # Importa las señales necesarias.

# Modelo que representa el carrito de compras.
class Cart(models.Model):
    # ID único para cada carrito, generado con UUID.
    cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
    
    # El carrito puede estar vinculado a un usuario, pero es opcional.
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    
    # Relación muchos a muchos con productos, utilizando un modelo intermedio `CartProducts`.
    products = models.ManyToManyField(Product, through='CartProducts')
    
    # Subtotal sin comisiones o impuestos.
    subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    
    # Total del carrito, incluyendo comisiones/impuestos.
    total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
    
    # Fecha de creación del carrito.
    create_at = models.DateTimeField(auto_now_add=True)

    # Comisión fija aplicada al total del carrito.
    FEE = 0.05

    # Representación en cadena del carrito.
    def __str__(self):
        return self.cart_id
    
    # Actualiza tanto el subtotal como el total del carrito.
    def update_totals(self):
        self.update_subtotal()
        self.update_total()

        # Si hay una orden vinculada al carrito, también actualiza el total de la orden.
        if self.order:
            self.order.update_total()

    # Calcula el subtotal sumando los precios de los productos por su cantidad.
    def update_subtotal(self):
        self.subtotal = sum([
            cp.quantity * cp.product.price  for cp in self.products_related()
        ])
        self.save()
    
    # Calcula el total añadiendo una comisión al subtotal.
    def update_total(self):
        self.total = self.subtotal + (self.subtotal * decimal.Decimal(Cart.FEE))
        self.save()

    # Retorna los productos relacionados con el carrito.
    def products_related(self):
        return self.cartproducts_set.select_related('product')
    
    # Verifica si el carrito tiene productos.
    def has_products(self):
        return self.products.exists()

    # Retorna la orden vinculada al carrito que esté en estado `CREATED`, si existe.
    @property
    def order(self):
        return self.order_set.filter(status=OrderStatus.CREATED).first()


# Manager personalizado para el modelo CartProducts.
class CartProductManager(models.Manager):
    
    # Crea o actualiza la cantidad de un producto en el carrito.
    def create_or_update_quantity(self, cart, product, quantity=1):
        object, created = self.get_or_create(cart=cart, product=product)

        # Si el producto ya estaba en el carrito, suma la cantidad nueva a la existente.
        if not created:
            quantity = object.quantity + quantity

        # Actualiza la cantidad del producto en el carrito.
        object.update_quantity(quantity)
        return object
    

# Modelo que representa los productos dentro de un carrito.
class CartProducts(models.Model):
    # Relación con el carrito.
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    
    # Relación con el producto.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # Cantidad del producto en el carrito.
    quantity = models.IntegerField(default=1)
    
    # Fecha de creación del registro de producto en el carrito.
    created_at = models.DateTimeField(auto_now_add=True)

    # Usa el manager personalizado definido previamente.
    objects = CartProductManager()

    # Actualiza la cantidad de un producto en el carrito.
    def update_quantity(self, quantity=1):
        self.quantity = quantity
        self.save()


# Señal para asignar un `cart_id` único antes de guardar un carrito.
def set_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())  # Genera un UUID único para el carrito.


# Señal que se activa cuando se añaden o quitan productos del carrito para actualizar los totales.
def update_Totals(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_totals()  # Recalcula los totales del carrito.


# Señal que se activa después de guardar un producto en el carrito para actualizar los totales.
def post_save_update_totals(sender, instance, *args, **kwargs):
    instance.cart.update_totals()  # Actualiza los totales del carrito.


# Conecta las señales a las funciones correspondientes.
pre_save.connect(set_cart_id, sender=Cart)  # Asigna el ID único antes de guardar el carrito.
post_save.connect(post_save_update_totals, sender=CartProducts)  # Actualiza totales después de añadir productos.
m2m_changed.connect(update_Totals, sender=Cart.products.through)  # Actualiza totales cuando cambian los productos del carrito.
