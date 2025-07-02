import uuid
from django.db import models
from django.conf import settings
from django.db.models import Sum
from products.models import Product  # Adjust this import according to your project structure


# Create your models here.
class Order(models.Model):
    """Model to represent an order in the checkout process."""
    order_number = models.CharField(max_length=32, unique=True, editable=False)
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True)
    address_line_1 = models.CharField(max_length=80)
    address_line_2 = models.CharField(max_length=80, blank=True)
    town_or_city = models.CharField(max_length=40)
    postcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=40)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.order_number
    
    def _generate_order_number(self):
        """Generate a unique order number."""
        return uuid.uuid4().hex.upper()
    
    def update_total(self):
        """Update the order total and grand total based on line items."""
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = settings.STANDARD_DELIVERY_Percentage / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """Override the save method to ensure the order number is generated."""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

class OrderLineItem(models.Model):
    """Model to represent a line item in an order."""
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(max_length=2, blank=True)
    quantity = models.IntegerField()
    lineitem_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def __str__(self):
        return f'{self.product.sku} on order {self.order.order_number}'
    
    def save(self, *args, **kwargs):
        """Override the save method to set the line item total."""
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
