# My Django imports
from django.contrib import admin

# My App imports
from OBMS_basics.models import Product, OrderItem, Order, BillingInformation, Payment

# Register your models here.
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(BillingInformation)
admin.site.register(Payment)