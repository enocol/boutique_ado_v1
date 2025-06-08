from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404
from django.http import Http404

# Create your views here.

def all_products(request):
    """ A view to return all products """

    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/all_products.html', context)

def product_detail(request, product_id):
    """ A view to return a single product """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
        'star_range': [1, 2, 3, 4, 5, 6],  # Assuming a 5-star rating system

    }

    return render(request, 'products/product_detail.html', context)