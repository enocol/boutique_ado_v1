from django.shortcuts import render, redirect, reverse
from .models import Product
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages

# Create your views here.

def all_products(request):
    """ A view to return all products """

    products = Product.objects.all()
    query = None
    if 'q' in request.GET:
        query = request.GET['q']
        if not query:
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('all_products'))
        
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        'products': products,
        'search_term': request.GET.get('q', ''),
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