from django.urls import reverse_lazy
# from django.views import View
# from django.shortcuts import render
# from django.core.paginator import Paginator

# from django.utils import timezone
# from django.views.generic import ListView, DetailView
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from typing import Any

from .models import Product
from .forms import ProductForm
from .filters import ProductFilter
# from datetime import datetime


class ProductsList(ListView):
    model = Product
    template_name = 'fastfood/products.html'
    # context_object_name = 'products'
    # В листинге в юните D4.3 этой строки нет
    form_class = ProductForm 
    # queryset = Product.objects.order_by('price')
    ordering = ['-price']
    paginate_by = 1

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # context['time_now'] = timezone.localtime(timezone.now())
        # context['value1'] = None
        # context['value2'] = {'field1': 'нового'}
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset())
        # context['choices'] = Product.TYPE_CHOICES
        context['form'] = ProductForm()
        return context
    
    def post(self, request, *args, **kwargs):
        # name = request.POST['name']
        # price = request.POST['price']
        # type = request.POST['type']
        # description = request.POST['description']
        # product = Product(type=type, name=name, price=price, description=description)
        # product.save()
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class ProductDetailView(DetailView):
    template_name = 'fastfood/product_detail.html'
    queryset = Product.objects.all()


class ProductCreateView(CreateView):
    template_name = 'fastfood/product_create.html'
    form_class = ProductForm


class ProductUpdateView(UpdateView):
    template_name = 'fastfood/product_create.html'
    form_class = ProductForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Product.objects.get(pk=id)


class ProductDeleteView(DeleteView):
    template_name = 'fastfood/product_delete.html'
    queryset = Product.objects.all()
    success_url = reverse_lazy('fastfood:products')


# class ProductDetail(DetailView):
#     model = Product
#     template_name = 'fastfood/product.html'
#     context_object_name = 'product'


# class Products(View):
#     def get(self, request):
#         products = Product.objects.order_by('-price')
#         p = Paginator(products, 1)
#         products = p.get_page(request.GET.get('page', 1))
#         data = { 
#             'products': products,
#             }
#         return render(request, 'fastfood/products.html', data)
