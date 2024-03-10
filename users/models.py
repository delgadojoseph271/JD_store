from stripeAPI .customer import create_customer

from django.db import models


from django.contrib.auth.models import AbstractUser

from orders.common import OrderStatus

# Create your models here.
class User(AbstractUser):
    customer_id = models.CharField(max_length=100, blank=True, null=True)
    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
    
    @property
    def shipping_address(self):
        return self.shippingaddress_set.filter(default=True).first()

    @property
    def billing_profile(self):
        return self.billingprofile_set.filter(default=True).first()

    @property
    def description(self):
        return 'descripcion para el usuario {}'.format(self.username)

    def has_billing_profile(self):
        return self.billingprofile_set.exist()
    
    def has_billing_profiles(self):
        return self.customer_id is not None

    def has_customer(self):
        return self.customer_id is not None
    
    def create_customer_id(self):
        if not self.has_customer():
            customer  =  create_customer(self)
            self.customer_id = customer.instance_url
            self.save()

    def has_shipping_address(self):
        return self.shipping_address is not None
    
    def orders_complete(self):
        return self.order_set.filter(status=OrderStatus.COMPLETED).order_by('-id')
    
    def has_shipping_addresses(self):
        return self.shippingaddress_set.exists()
    
    @property
    def addresses(self):
        return self.shippingaddress_set.all()
    
    def billing_profiles(self):
        return self.billingprofiles_set.all().order_by('-default')

class Customer(User):
    class Meta:
        proxy = True

    def get_products(self):
        return []
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()