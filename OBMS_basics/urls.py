# Django Imports
from django.urls import path

# My app imports
from OBMS_basics.views import (
    HomeView,
    AboutView,
    ContactView,
    ProductView,
)

app_name = 'basics'

urlpatterns = [
    # Static pages
    path('', HomeView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),
    path('product', ProductView.as_view(), name='product'),
]