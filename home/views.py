from django.shortcuts import render

# Create your views here.

def home(request):
    """
    Render the home page of the boutique.
    """
    if 'search' in request.GET:
        print('search =' ' search')


        
    return render(request, 'home/home.html')
