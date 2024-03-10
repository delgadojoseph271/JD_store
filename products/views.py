from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.db.models import Q


from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from products.models import Product
# Create your views here.


class ProductListView(ListView):
    template_name = 'index.html'
    queryset = Product.objects.all().order_by('id')
    paginate_by = 1

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['message']= 'Listado de Producto'

        return context
    
class ProductDetailView(DetailView): 
    model = Product
    template_name = 'products/product.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)

        print(context)
        return context
    
class ProductSearchListView(ListView):
    template_name = 'products/search.html'

    def get_queryset(self):
        filters = Q(title__icontains=self.query()) | Q(category__title__icontains=self.query())
        return Product.objects.filter(filters)

    def query(self):

        return self.request.GET.get('q')
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['query']= self.query()
        context['count'] = context['product_list'].count()

        print(context)
        return context



