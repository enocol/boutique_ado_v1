from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from decimal import Decimal as decimal

def bag_contents(request):
    """ A view to return the shopping bag contents """

    Free_delivery_threshold = decimal(settings.FREE_DELIVERY_THRESHOLD)
    bag_items = []
    product_count = 0
    total = 0
    bag = request.session.get('bag', {})
    # Iterate through the bag items to calculate total price and product count
            

    for item_id , item_data in bag.items():
      
        if isinstance(item_data, int):
           
            product = get_object_or_404(Product, pk=item_id)
            line_total = item_data * product.price
            total += item_data * decimal(product.price)
            product_count += item_data
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
                'price': product.price,
                'total_price': total
                
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * decimal(product.price)
                line_total = quantity * product.price
                size = size
                # Add the item to the bag items list
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'price': product.price,
                    'total_price': total,
                    'size': size,
                    'line_total': line_total
                    
                })
            print(bag_items)
        
    if total < Free_delivery_threshold:
        delivery_cost = decimal(5.00)
    else:
        delivery_cost = 0

    context = {
        'free_delivery_threshold': Free_delivery_threshold,
        'bag_items': bag_items,
        'product_count': product_count,
        'total': total,
        'delivery_cost': delivery_cost,
        'delivery_cost_threshold': Free_delivery_threshold - total if total < Free_delivery_threshold else 0,
       
    }
    context['grand_total'] = total + delivery_cost
    context['free_delivery'] = total >= Free_delivery_threshold
    return context