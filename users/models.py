from stripeAPI.customer import create_customer  # Función para crear un cliente en Stripe
from django.db import models  # Importa las herramientas para definir modelos
from django.contrib.auth.models import AbstractUser  # Modelo de usuario personalizado
from orders.common import OrderStatus  # Importa los estados de órdenes

# Modelo personalizado User que extiende AbstractUser
class User(AbstractUser):
    customer_id = models.CharField(max_length=100, blank=True, null=True)  # ID del cliente en Stripe, opcional
    
    def get_full_name(self):
        """Devuelve el nombre completo del usuario."""
        return '{} {}'.format(self.first_name, self.last_name)
    
    @property
    def shipping_address(self):
        """Devuelve la dirección de envío predeterminada del usuario, si existe."""
        return self.shippingaddress_set.filter(default=True).first()

    @property
    def billing_profile(self):
        """Devuelve el perfil de facturación predeterminado del usuario."""
        return self.billingprofile_set.filter(default=True).first()

    @property
    def description(self):
        """Devuelve una descripción personalizada del usuario."""
        return 'descripcion para el usuario {}'.format(self.username)

    def has_billing_profile(self):
        """Verifica si el usuario tiene un perfil de facturación."""
        return self.billingprofile_set.exists()
    
    def has_billing_profiles(self):
        """Verifica si el usuario tiene perfiles de facturación en Stripe."""
        return self.customer_id is not None

    def has_customer(self):
        """Devuelve True si el usuario tiene un ID de cliente en Stripe."""
        return self.customer_id is not None
    
    def create_customer_id(self):
        """Crea un ID de cliente en Stripe si no existe y lo guarda."""
        if not self.has_customer():
            customer = create_customer(self)
            self.customer_id = customer.instance_url
            self.save()

    def has_shipping_address(self):
        """Verifica si el usuario tiene una dirección de envío predeterminada."""
        return self.shipping_address is not None
    
    def orders_complete(self):
        """Devuelve todas las órdenes completadas del usuario."""
        return self.order_set.filter(status=OrderStatus.COMPLETED).order_by('-id')
    
    def has_shipping_addresses(self):
        """Verifica si el usuario tiene al menos una dirección de envío."""
        return self.shippingaddress_set.exists()
    
    @property
    def addresses(self):
        """Devuelve todas las direcciones de envío del usuario."""
        return self.shippingaddress_set.all()
    
    def billing_profiles(self):
        """Devuelve todos los perfiles de facturación del usuario, ordenados por si son predeterminados."""
        return self.billingprofile_set.all().order_by('-default')

# Modelo proxy Customer que extiende User
class Customer(User):
    class Meta:
        proxy = True  # Define este modelo como proxy

    def get_products(self):
        """Devuelve una lista de productos (actualmente vacío)."""
        return []

# Modelo Profile que extiende el perfil de usuario
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación uno a uno con el usuario
    bio = models.TextField()  # Campo de biografía para el usuario
