from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def bag_contents(request):
    """ A view to return the shopping bag contents """

    Free_delivery_threshold = settings.FREE_DELIVERY_THRESHOLD
    bag_items = []
    product_count = 0
    total = 0
    bag = request.session.get('bag', {})
    for item_id, quantity in bag.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * int(product.price)
        product_count += quantity
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
            'price': product.price,
            'total_price': quantity * product.price,
        })
    if product_count < Free_delivery_threshold:
        delivery_cost = 5.00
    else:
        delivery_cost = 0

    context = {
        'free_delivery_threshold': Free_delivery_threshold,
        'bag_items': bag_items,
        'product_count': product_count,
        'total': total,
        'delivery_cost': delivery_cost,
    }
    context['grand_total'] = total + delivery_cost
    context['free_delivery'] = total >= Free_delivery_threshold
    return context