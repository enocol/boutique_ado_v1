from django import forms
from .models import Order  # Adjust this import according to your project structure

class CheckoutForm(forms.ModelForm):
    """Form for the checkout process."""
    
    class Meta:
        model = Order  # Replace with your Order model
        fields = [
            'full_name', 'email', 'phone_number', 'country',
            'postcode', 'town_or_city', 'address_line_1',
            'address_line_2', 'country'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postcode',
            'town_or_city': 'Town or City',
            'address_line_1': 'Street Address 1',
            'address_line_2': 'Street Address 2 (optional)',
            'county': 'County (optional)',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field in placeholders:
                placeholder_text = placeholders[field]
                if self.fields[field].required:
                    placeholder_text += ' *'
                self.fields[field].widget.attrs['placeholder'] = placeholder_text
            # Default class and hide label
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False