from django.contrib import messages
from django.shortcuts import redirect, render, reverse, get_object_or_404

from checkout.models import Order
from .forms import CheckoutForm
from bag.contexts import bag_contents
from products.models import Product
from checkout.models import OrderLineItem

from django.shortcuts import get_object_or_404


from django.conf import settings

import stripe

# Create your views here.
def checkout(request):
    """ A view to return the checkout page """
    stripe_secret_key = settings.STRIPE_SECRET_KEY  # Set your Stripe secret key
    stripe_public_key = settings.STRIPE_PUBLIC_KEY  # Set your Stripe public key

    

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty. Please add items to your bag before checking out.")
        return redirect(reverse('all_products'))
    # Get the bag contents
    current_bag = bag_contents(request)
    total = current_bag['total']
    stripe_total = round(total * 100)  # Convert to cents for Stripe
    stripe.api_key = stripe_secret_key  # Set the Stripe secret key

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,  # Set your desired currency
        payment_method_types=['card'],
    )
    
    checkoutForm = CheckoutForm()

    if not stripe_public_key:
        messages.error(request, "Stripe public key is not set. Please check your settings.")
        return redirect(reverse('products'))
    template = 'checkout/checkout.html'
    context = {
        'checkoutForm': checkoutForm,
        'stripe_public_key': stripe_public_key,  # Replace with your actual Stripe public key
        'client_secret': intent.client_secret,  # Replace with your actual Stripe client secret
    }

    return render(request, template, context)






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
