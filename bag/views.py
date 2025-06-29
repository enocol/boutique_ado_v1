from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product  # adjust this according to your project

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
            messages.success(request, f'Added {quantity} of size {size} of item {item_id} to your bag.')
          else:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Added {quantity} of size {size} of item {item_id} to your bag.')
        else:
           bag[item_id] = {'items_by_size': {size: quantity}}
        messages.success(request, f'Added {quantity} of size {size} of item {item_id} to your bag.')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Added {quantity} of item {item_id} to your bag.')
        else:
            bag[item_id] = quantity 
            messages.success(request, f'Added {quantity} of item {item_id} to your bag.')
    redirect_url = request.POST.get('redirect_url')
    
    # Save the updated session back to the request
    request.session['bag'] = bag

    # Redirect back to the specified URL
    return redirect(redirect_url)


@require_POST
def adjust_bag(request, item_id):
    """ Adjust the quantity of the specified product to the shopping bag """
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size', None)

    bag = request.session.get('bag', {})
    if size:
        if item_id in bag and 'items_by_size' in bag[item_id]:
            if size in bag[item_id]['items_by_size']:
                if quantity > 0:
                    bag[item_id]['items_by_size'][size] = quantity  
                else:
                    del bag[item_id]['items_by_size'][size] 
                if not bag[item_id]['items_by_size']:
                    del bag[item_id]    
    else:
        if item_id in bag:
            if quantity > 0:
                bag[item_id] = quantity  
            else:
                del bag[item_id]
    # Save the updated session back to the request
    request.session['bag'] = bag
    messages.success(request, f'Updated {item_id} quantity to {quantity}.')

    # Redirect back to the bag page
    return redirect('bag')


def remove_from_bag(request, item_id, size=None):
    """Remove a specific size of an item from the shopping bag, or the whole item if no size is specified."""
    bag = request.session.get('bag', {})
    item_id = str(item_id)
    size = request.GET.get('size', None)  # Get size from query parameters if not provided

    if item_id in bag:
        if size:
            # Only remove the specific size
            if size in bag[item_id]['items_by_size']:
                del bag[item_id]['items_by_size'][size]
                messages.success(request, f"Removed size {size.upper()} of item {item_id} from your bag.")

                # If no sizes left, remove the item completely
                if not bag[item_id]['items_by_size']:
                    del bag[item_id]
                    messages.success(request, f"All sizes of item {item_id} removed from your bag.")
            else:
                messages.warning(request, f"Size {size.upper()} of item {item_id} not found in your bag.")
        else:
            # If no size is given, remove the whole item
            del bag[item_id]
            messages.success(request, f"Removed item {item_id} from your bag.")
    else:
        messages.error(request, f"Item {item_id} not found in your bag.")

    request.session['bag'] = bag
    return redirect('bag')  # Replace with your actual bag view name


