from django.shortcuts import render, redirect, reverse
from .models import Product
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q

from django.db.models.functions import Lower

# Create your views here.

def all_products(request):
    """ A view to return all products with sorting, searching and filtering """
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    sortkey = None

    # Search logic
    if 'q' in request.GET:
        query = request.GET['q']
        if query:
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
        else:
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('all_products'))

    # Category filtering
    if 'category' in request.GET:
        categories = request.GET.get('category').split(',')
        if not categories:
            messages.error(request, "You didn't select any categories!")
            return redirect(reverse('all_products'))
       
        if categories:
            products = products.filter(category__name__in=categories)

    # Sorting logic
    if 'sort' in request.GET:
        sort = request.GET['sort']
        direction = request.GET.get('direction', 'asc')
        
        if sort == 'name':
            sortkey = 'name'
        elif sort == 'price':
            sortkey = 'price'
        elif sort == 'rating':
            sortkey = 'rating'
        elif sort == 'category':
            sortkey = 'category__name'
        else:
            messages.error(request, "Invalid sort option!")
            return redirect(reverse('all_products'))

        if sortkey:
            if direction == 'desc':
                sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    context = {
        'products': products,
        'current_sort': f'{sort}_{direction}' if sort else '',
        'categories': categories,
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