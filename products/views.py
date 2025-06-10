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
    categories = None


    if 'q' in request.GET:
        query = request.GET['q']
        if query:
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
            categories = products.filter(category__name__icontains=query)
        else:
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('all_products'))

       
        
    

    if 'category' in request.GET:
        categories = request.GET['category'].split(',')
        print('categories===', categories)
        
        if categories:
            products = products.filter(category__name__in=categories)
            categories = Product.objects.filter(category__name__in=categories).distinct()
        else:
            messages.error(request, "You didn't select any categories!")
            return redirect(reverse('all_products'))
        
       
       
        
        

    context = {
        'products': products,
        'categories': categories,
        'star_range': range(1, 6),  # Add this line so you can loop from 1 to 5 in your template
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