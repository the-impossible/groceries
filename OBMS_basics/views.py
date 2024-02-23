#Django Imports
from django.shortcuts import render, get_object_or_404, render, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import DetailView, ListView
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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
        if request.user.is_authenticated:
            return redirect('auth:all_products')
        return render(request,'basics/product.html', context)

class ProductDetailView(DetailView):
    model = Product
    template_name = "basics/product_detail.html"

class OrderSummaryView(View):
    def get(self, request):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'orders': order
            }
        except ObjectDoesNotExist:
            messages.error(request, 'You do not have an active order')
            return redirect('basics:product')
        return render(request, 'basics/order_summary.html', context)

class ContactView(View):
    def get(self, request):
        return render(request,'basics/contact.html')

@login_required(login_url='/auth/login')
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    # user_id = request.session['nonuser']

    order_item, created = OrderItem.objects.get_or_create(user=request.user, completed=False, product=product)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    # order_item, created = OrderItem.objects.get_or_create(session_id=user_id, completed=False, product=product)
    # order_qs = Order.objects.filter(session_id=user_id, ordered=False)

    # Performing QUANTITY validation
    requested_quantity = 0
    calculated_quantity = 0

    if created:
        calculated_quantity += order_item.quantity
    else:
        calculated_quantity += order_item.quantity

    try:
        quantity = int(request.POST.get('quantity'))
        requested_quantity = quantity
        calculated_quantity += quantity
    except TypeError:
        requested_quantity += 1

    if calculated_quantity > product.quantity:
        messages.error(request, 'Quantity requested for is greater than available quantity')
        if request.user.is_authenticated:
            return redirect('auth:product_details', slug=slug)
        else:
            return redirect('auth:product_detail', slug=slug)

    if order_qs.exists():
        order = order_qs[0]
        if order.product.filter(product__slug=product.slug).exists():
            order_item.quantity += requested_quantity
            order_item.save()
            messages.success(request, "This Product quantity was updated!")
        else:
            messages.success(request, "This Product has been added to Cart!")
            order.product.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, order_date=ordered_date)
        order.product.add(order_item)
        messages.success(request, "This Product has been added to Cart!")

    if request.user.is_authenticated:
        return redirect('auth:product_details', slug=slug)
    else:
        return redirect('auth:product_detail', slug=slug)

@login_required(login_url='/auth/login')
def remove_from_cart(request, slug, mode='single'):
    product = get_object_or_404(Product, slug=slug)
    # user_id = request.session['nonuser']

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.product.filter(product__slug=product.slug).exists():
            order_item = OrderItem.objects.filter(user=request.user, completed=False, product=product)[0]

            if mode == 'all':
                order_item.delete()
                order.product.remove(order_item)
                messages.info(request, "This Product has been remove from Cart!")
            else:
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.info(request, "The Product quantity has been updated!")
                else:
                    order.product.remove(order_item)
                    messages.info(request, "This Product has been remove from Cart!")
            return redirect('auth:order_summary')
        else:
            messages.info(request, "This Product is not in your Cart!")
    else:
        messages.info(request, "User don't have an active order")
    return redirect('auth:all_products')

class SearchProductView(ListView):
    model = Product
    template_name = "auth/search.html"

    def get_queryset(self):
        qs = self.request.GET.get('qs')
        result = (
            Product.objects.filter(title__icontains=qs) |
            Product.objects.filter(description__icontains=qs) |
            Product.objects.filter(slug__icontains=qs)
        )
        return result

    def get_context_data(self, **kwargs):
        context = super(SearchProductView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('qs')
        return context

