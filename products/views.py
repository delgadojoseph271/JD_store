from typing import Any  # Anotaciones de tipos opcionales
from django.db.models.query import QuerySet  # Anotaciones de tipos para QuerySet
from django.shortcuts import render  # Para renderizar plantillas
from django.db.models import Q  # Para construir consultas complejas

from django.views.generic.list import ListView  # Vista genérica para listar objetos
from django.views.generic.detail import DetailView  # Vista genérica para detalles de objetos

from products.models import Product  # Modelo de producto

from pprint import pprint

# Vista para listar productos
class ProductListView(ListView):
    template_name = 'index.html'  # Plantilla a utilizar
    queryset = Product.objects.all().order_by('id')  # Lista de productos, ordenados por 'id'
    paginate_by = 3  # Muestra 1 producto por página

    # Añadir datos adicionales al contexto de la vista
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Obtener el contexto básico
        print("\n\n\n")
        pprint( context)
        print("\n\n\n")
        context['message'] = 'Listado de Producto'  # Mensaje personalizado
        print("\n\n\n")
        pprint( context)
        print("\n\n\n")

        return context

# Vista para mostrar los detalles de un producto
class ProductDetailView(DetailView):
    model = Product  # Modelo que se mostrará
    template_name = 'products/product.html'  # Plantilla para el detalle del producto

    # Añadir datos adicionales al contexto de la vista
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Obtener el contexto básico
        print(context)  # Imprimir contexto para depuración
        return context

# Vista para buscar productos
class ProductSearchListView(ListView):
    template_name = 'products/search.html'  # Plantilla para los resultados de búsqueda

    # Filtrar los productos según el término de búsqueda
    def get_queryset(self):
        filters = Q(title__icontains=self.query()) | Q(category__title__icontains=self.query())  # Filtra por título o categoría
        return Product.objects.filter(filters)  # Retorna el queryset filtrado

    # Extraer el término de búsqueda desde los parámetros GET
    def query(self):
        return self.request.GET.get('q')  # Retorna el valor de 'q' en la URL

    # Añadir datos adicionales al contexto de la vista
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Obtener el contexto básico
        context['query'] = self.query()  # Añadir el término de búsqueda al contexto
        context['count'] = context['product_list'].count()  # Contar los productos encontrados
        print(context)  # Imprimir contexto para depuración
        return context
