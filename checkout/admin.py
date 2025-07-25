from django.contrib import admin
from .models import Order, OrderLineItem

# Register your models here.

class OrderLineItemAdminInline(admin.TabularInline):
    """Admin for OrderLineItem."""
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
   

class OrderAdmin(admin.ModelAdmin):
    """Admin for Order."""
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number','date', 'delivery_cost', 'order_total', 'grand_total')
    fields = ('order_number', 'date', 'full_name', 'town_or_city', 'order_total', 'delivery_cost', 'grand_total')
    list_display = ('order_number', 'date', 'full_name', 'order_total', 'delivery_cost', 'grand_total')
    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)

