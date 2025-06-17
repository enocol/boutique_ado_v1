from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.

def bag(request):
    """ A view to return the shopping bag """
    return render(request, 'bag/bag.html')






def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not specified
    if quantity < 1:
        quantity = 1  # Ensure quantity is at least 1
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})
    if item_id in bag:
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    # Save the updated session back to the request
    request.session['bag'] = bag

    # Redirect back to the specified URL
    return redirect(redirect_url)