# My django app imports
from django.db import models
from django.shortcuts import reverse

# My app imports
from OBMS_auth.models import Accounts

# Create your models here.
# My entire products
class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)
    description = models.TextField()
    slug = models.SlugField(null=False, unique=True)
    image = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("basics:product_detail", kwargs={
            'slug':self.slug
        })


    def get_add_to_cart_url(self):
        return reverse("basics:add_to_cart", kwargs={
            'slug':self.slug
        })

    def remove_from_cart(self):
        return reverse("basics:remove_from_cart", kwargs={
            'slug':self.slug
        })

# Product currently been added to CART
class OrderItem(models.Model):
    user = models.ForeignKey(to=Accounts, on_delete=models.CASCADE, blank=True, null=True)
    completed = models.BooleanField(default=False)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'

    def get_total_item_price(self):
        return self.quantity * self.product.price

# product assigned to an ORDER
class Order(models.Model):
    user = models.ForeignKey(to=Accounts, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ManyToManyField(OrderItem)
    order_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing = models.ForeignKey('BillingInformation', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}'

    def get_total(self):
        return sum([order_item.get_total_item_price() for order_item in self.product.all()])

    def get_total_quantity(self):
        return sum([order_item.quantity for order_item in self.product.all()])

class BillingInformation(models.Model):
    user = models.ForeignKey(to=Accounts, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.address}'

class Payment(models.Model):
    user = models.ForeignKey(to=Accounts, on_delete=models.CASCADE, blank=True, null=True)
    stripe_charge_id = models.CharField(max_length=50, blank=True, null=True)
    amount = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} purchase goods worth: {self.amount}'