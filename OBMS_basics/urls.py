# Django Imports
from django.urls import path

# My app imports
from OBMS_basics.views import (
    HomeView,
    AboutView,
    ContactView,
    ProductView,
    add_to_cart,
    remove_from_cart,
    ProductDetailView,
    OrderSummaryView,
    SearchProductView,
)

app_name = 'basics'

urlpatterns = [
    # Static pages
    path('', HomeView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('contact', ContactView.as_view(), name='contact'),

    # PRODUCT
    path('product', ProductView.as_view(), name='product'),
    path('product_detail/<slug>/', ProductDetailView.as_view(), name='product_detail'),

    # CART
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/<str:mode>', remove_from_cart, name='remove_from_cart'),
    path('order_summary', OrderSummaryView.as_view(), name='order_summary'),

    # SEARCH
    path('search', SearchProductView.as_view(), name='search'),
]