from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.

def bag(request):
    """ A view to return the shopping bag """
    return render(request, 'bag/bag.html')






def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """
    quantity = int(request.POST.get('quantity', 1))  # Default to 1 if not specified
    size = None
    bag = request.session.get('bag', {})
   
    if 'size in request.POST':
        size = request.POST.get('size', None)

    if size:
        if item_id in list(bag.keys()):
          if size in bag[item_id]['items_by_size'].keys():
            bag[item_id]['items_by_size'][size] += quantity
          else:
            bag[item_id]['items_by_size'][size] = quantity
        else:
           bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity 
    redirect_url = request.POST.get('redirect_url')
    
    # Save the updated session back to the request
    request.session['bag'] = bag

    # Redirect back to the specified URL
    return redirect(redirect_url)