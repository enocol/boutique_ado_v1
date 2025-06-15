from django.conf import settings

def bag_contents(request):
    """ A view to return the shopping bag contents """

    Free_delivery_threshold = settings.FREE_DELIVERY_THRESHOLD
    context = {
        'free_delivery_threshold': Free_delivery_threshold,
        'bag_items': [],
        'total': 0,
        }
    return context