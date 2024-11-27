import uuid  # Para generar identificadores únicos
from django.db import models  # Herramientas para definir modelos en Django
from django.db.models.signals import pre_save  # Señal que se dispara antes de guardar un objeto
from django.utils.text import slugify  # Convierte texto en formato slug

# Modelo Product para representar un producto en la tienda
class Product(models.Model):
    title = models.CharField(max_length=50)  # Título del producto (máximo 50 caracteres)
    description = models.TextField()  # Descripción del producto
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)  # Precio del producto con 2 decimales
    slug = models.SlugField(null=False, blank=False, unique=True)  # Slug único basado en el título
    image = models.ImageField(upload_to='products/', null=False, blank=False)  # Imagen del producto
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación (se asigna automáticamente)

    def __str__(self):
        """Devuelve el título del producto como representación en cadena."""
        return self.title

# Función que genera un slug único antes de guardar el producto
def set_slug(sender, instance, *args, **kwargs):
    """Genera un slug basado en el título del producto si no existe uno."""
    if instance.title and not instance.slug:
        slug = slugify(instance.title)  # Convierte el título a formato slug
        
        # Si el slug ya existe, añade una cadena única para evitar duplicados
        while Product.objects.filter(slug=slug).exists():
            slug = slugify('{}-{}'.format(instance.title, str(uuid.uuid4())[:8]))
    
    instance.slug = slug  # Asigna el slug generado al producto

# Conecta la señal pre_save con el modelo Product para generar el slug antes de guardar
pre_save.connect(set_slug, sender=Product)
