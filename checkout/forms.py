from django import forms
from .models import Order  # Adjust this import according to your project structure

class CheckoutForm(forms.ModelForm):
    """Form for the checkout process."""
    
    class Meta:
        model = Order  # Replace with your Order model
        fields = [
            'full_name', 'email', 'phone_number', 'country',
            'postcode', 'town_or_city', 'street_address1',
            'street_address2', 'county'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholder = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postcode',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2 (optional)',
            'county': 'County (optional)',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field.self.fields[field].required:
                placeholder[field] += ' *'
            else:
                placeholder = placeholder[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
