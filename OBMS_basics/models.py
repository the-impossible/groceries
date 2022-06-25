# My django app imports
from django.db import models

# My app imports

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    slug = models.SlugField()
    image = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("basics:product", kwargs={
            'slug':self.slug
        })

class OrderItem(models.Model):
    # user = models.ForeignKey(to, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    session_id = models.CharField(max_length=200)