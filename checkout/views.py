from django.contrib import messages
from django.shortcuts import redirect, render, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST

from checkout.models import Order
from .forms import CheckoutForm
from bag.contexts import bag_contents
from products.models import Product
from checkout.models import OrderLineItem
import json

from django.shortcuts import get_object_or_404


from django.conf import settings

import stripe
# @require_POST
# def cached_checkout_data(request):
#     """ A utility function to retrieve cached checkout data """
#     pid = request.POST.get('client_secret').split('_secret')[0]
   
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     try:
#         stripe.PaymentIntent.modify(pid, metadata={
#             'username': request.user.username if request.user.is_authenticated else 'AnonymousUser',
#             'bag': json.dumps(request.session.get('bag', {})),
#             'save_info': request.session.get('save_info', False),
#             })
#         return HttpResponse(status=200)
#     except Exception as e:
#         messages.error(request, 'Your payment can not be processed now. Please try again.')
#         return HttpResponse(content=str(e), status=400)
    

@require_POST
def cached_checkout_data(request):
    """A utility function to retrieve cached checkout data"""
    try:
        data = json.loads(request.body)  # Parse JSON from request body

        client_secret = data.get('client_secret')
        if not client_secret:
            return HttpResponse("Missing client_secret", status=400)

        pid = client_secret.split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'username': request.user.username if request.user.is_authenticated else 'AnonymousUser',
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.session.get('save_info', False),
        })

        return HttpResponse(status=200)

    except Exception as e:
        # Optionally log the exception
        messages.error(request, 'Your payment cannot be processed right now. Please try again.')
        # Return a response with the error message
        return HttpResponse(content=f"Error caching checkout data: {str(e)}", status=400)


# Create your views here.
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST.get('full_name', ''),
            'email': request.POST.get('email', ''),
            'town_or_city': request.POST.get('town_or_city', ''),
            'postcode': request.POST.get('postcode', ''),
            'address_line_1': request.POST.get('address_line_1', ''),
            'address_line_2': request.POST.get('address_line_2', ''),
            'country': request.POST.get('country', ''),
        }

        order_form = CheckoutForm(form_data)
        if order_form.is_valid():
            order = order_form.save()
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!"
                    ))
                    order.delete()
                    return redirect(reverse('bag'))

            request.session['order_number'] = order.order_number
            request.session['save_info'] = 'save-info' in request.POST
            messages.success(request, f'Order {order.order_number} has been successfully created!')
            return redirect(reverse('checkout_success', args=[order.order_number]))

        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')

            # Stripe client_secret must still be passed again
            stripe.api_key = stripe_secret_key
            current_bag = bag_contents(request)
            total = current_bag['grand_total']
            stripe_total = round(total * 100)
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )

            context = {
                'checkoutForm': order_form,
                'stripe_public_key': stripe_public_key,
                'client_secret': intent.client_secret,
            }
            return render(request, 'checkout/checkout.html', context)

    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment.")
            return redirect(reverse('all_products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        order_form = CheckoutForm()

    if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    context = {
            'checkoutForm': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

    return render(request, 'checkout/checkout.html', context)





def checkout_success(request, order_number):
    """ A view to handle successful checkout """

    safe_info = request.session.get('safe_info', False)
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order {order.order_number} has been successfully processed! your order number is {order.order_number}. An email confirmation will be sent to {order.email}.')
    
    # Clear the bag from the session
    if 'bag' in request.session:
        del request.session['bag']
    
    context = {
        'order': order,
    }
    
    return render(request, 'checkout/checkout_success.html', context)
