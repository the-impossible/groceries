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
    slug = models.SlugField()
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
    session_id = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.quantity} of {self.product.title}'

# product assigned to an ORDER
class Order(models.Model):
    user = models.ForeignKey(to=Accounts, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ManyToManyField(OrderItem)
    order_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    session_id = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.session_id}'