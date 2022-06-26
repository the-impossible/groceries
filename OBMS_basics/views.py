#Django Imports
from django.shortcuts import render, get_object_or_404, render, redirect
from django.contrib import messages
from django.views import View
from django.utils import timezone

#My App imports
from OBMS_basics.models import Product, OrderItem, Order
class HomeView(View):
    def get(self, request):
        products = Product.objects.all().order_by('-id')

        context = {
            'products':products,
        }
        return render(request,'basics/index.html', context)

class AboutView(View):
    def get(self, request):
        return render(request,'basics/about.html')

class ProductView(View):
    def get(self, request):
        products = Product.objects.all().order_by('-id')

        context = {
            'products':products,
        }
        return render(request,'basics/product.html', context)

class ContactView(View):
    def get(self, request):
        return render(request,'basics/contact.html')

class DashboardView(View):
    def get(self, request):
        return render(request,'auth/dashboard.html')

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    user_id = request.session['nonuser']

    order_item, created = OrderItem.objects.get_or_create(session_id=user_id, completed=False, product=product)

    order_qs = Order.objects.filter(session_id=user_id, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.product.filter(product__slug=product.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, "This Product quantity was updated!")
        else:
            messages.success(request, "This Product has been added to Cart!")
            order.product.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(session_id=user_id, order_date=ordered_date)
        order.product.add(order_item)
        messages.success(request, "This Product has been added to Cart!")
    # Return to the product detail page
    return redirect('basics:product')

def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    user_id = request.session['nonuser']

    order_qs = Order.objects.filter(session_id=user_id, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.product.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(session_id=user_id, completed=False, product=product)[0]
            order_item.delete()
            order.product.remove(order_item)
            messages.info(request, "This Product has been remove from Cart!")
        else:
            messages.info(request, "This Product is not in your Cart!")
    else:
        messages.info(request, "User don't have an active order")
        # Return to the product detail page
    return redirect('basics:product')
