from django import forms
from .models import Order  # Adjust this import according to your project structure
from django_countries.fields import CountryField

class CheckoutForm(forms.ModelForm):
    """Form for the checkout process."""
 

    class Meta:
        model = Order  # Replace with your Order model
        fields = (
            'full_name', 'email',
            'postcode', 'town_or_city', 'address_line_1',
            'address_line_2', 'country'
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'postcode': 'Postcode',
            'town_or_city': 'Town or City',
            'address_line_1': 'Street Address 1',
            'address_line_2': 'Street Address 2 (optional)',
            'country': 'Country',
            
        }

       

        self.fields['full_name'].widget.attrs['autofocus'] = True
        self.fields['country'].widget.attrs.update({
            'class': 'form-select'
        })
        for field in self.fields:
            if field in placeholders:
                placeholder_text = placeholders[field]
                if self.fields[field].required:
                    placeholder_text += ' *'
                self.fields[field].widget.attrs['placeholder'] = placeholder_text
            # Default class and hide label
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False

        
       