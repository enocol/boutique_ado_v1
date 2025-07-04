from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, reverse
from .forms import CheckoutForm

# Create your views here.
def checkout(request):
    """ A view to return the checkout page """

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty. Please add items to your bag before proceeding to checkout.")
        return redirect(reverse('products'))
    checkoutForm = CheckoutForm()
    context = {
        'checkoutForm': checkoutForm,
        'stripe_public_key': 'pk_test_51RhEdzFYdUWqTKqwR4AvdHBvdQCz4nNxquKUzqpEKiQSFXKBkRC5lgGJTwACoWeDM4HZt3FWkhVEUJyZHJMWtSm100Y4PoW6pd',  # Replace with your actual Stripe public key
        'client_secret': 'test_client_secret',  # Replace with your actual Stripe client secret
    }

    return render(request, 'checkout/checkout.html', context)
