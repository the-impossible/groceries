# My django imports
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin

# My app imports
from OBMS_auth.forms import AccountCreationForm, EditAccountCreationForm, BillingForm
from OBMS_auth.models import Accounts
from OBMS_basics.models import Product, Order, BillingInformation, Payment, OrderItem
from OBMS_auth.forms import AddProductForm
# To_PDF
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
# Payment
import stripe
stripe.api_key = "sk_test_51L5Xs6GCAqCizi1RncjTC84yc0J7jaecLFB5gj07ZDNWCREFyEylsunXTltlQleL3lWzEcLsqIFCInvn6wGYu2Xa00cIHRZjMz"

# Create your views here.
class DashboardView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    def get(self, request):
        happy = Order.objects.filter(delivered=True).count() / 100

        context = {
            'customers':Accounts.objects.filter(is_staff=False).count(),
            'happy':happy,
            'products':Product.objects.all().count(),
            'amount_sold':sum([amount.amount for amount in Payment.objects.all()]),
        }
        return render(request,'auth/dashboard.html', context)

class RegisterView(SuccessMessageMixin, CreateView):
    model = Accounts
    form_class = AccountCreationForm
    template_name = 'auth/register.html'
    success_message = "Account created successfully, you can now login!!"

    def get_success_url(self):
        return reverse("auth:login")

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data.get('password'))
        form.instance.email = form.cleaned_data.get('email').strip().lower()
        return super().form_valid(form)

class LoginView(View):
    def get(self, request):
        context = {
            'next': request.GET.get('next', None)
        }
        return render(request, 'auth/login.html', context)

    def post(self, request):
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')

        if email and password:
            # Authenticate user
            user = authenticate(request, email=email, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'You are now signed in {user.get_name()}')
                    return redirect('auth:dashboard')
                else:
                    messages.warning(request, 'Account not active contact the administrator')
                    return redirect('auth:login')
            else:
                messages.warning(request, 'Invalid login credentials')
                return redirect('auth:login')
        else:
            messages.error(request, 'All fields are required!!')
            return redirect('auth:login')

class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.success(request, 'You are now signed out!')
        return redirect('auth:login')

class ProfileView(LoginRequiredMixin, View):
    login_url = '/auth/login'
    def get(self, request, user_id):
        user = get_object_or_404(Accounts, id=user_id)
        orders = Order.objects.filter(user=request.user).count()
        form = EditAccountCreationForm(instance=user)
        context = {
            'form':form,
            'orders':orders,
            'user':user,
        }
        return render(request,'auth/profile.html', context)

    def post(self, request, user_id):
        user = get_object_or_404(Accounts, id=user_id)
        form = EditAccountCreationForm(request.POST, request.FILES, instance=user)

        if 'profile' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('auth:profile', user_id)
            else:
                messages.error(request, 'Error updating Profile!')
            context = {
                'form':form,
                'user':user,
            }
        else:
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            context = {
                'form':form,
                'user':user,
            }

            if password1 and password2:
                if password1 != password2:
                    messages.error(request, 'Passwords does not match!')
                    return redirect('auth:profile', user_id)

                if len(password1) < 6 :
                    messages.error(request, 'Password too short, ensure at least 6 characters!')
                    return redirect('auth:profile', user_id)

                user.set_password(password1)
                user.save()

                messages.success(request, 'Password reset successful!!')
                if request.user == user:
                    return redirect('auth:login')

                if request.user.is_superuser:
                    return redirect('auth:profile', user_id)
                return redirect('auth:login')

        return render(request,'auth/profile.html', context)

class AllProductsListView(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = Product
    paginate_by = 8
    template_name = "auth/all_products.html"
    ordering = ['-id']

    def get_queryset(self):
        return Product.objects.filter(quantity__gte=1).order_by('-id')

class ProductDetailListView(LoginRequiredMixin, DetailView):
    login_url = '/auth/login'
    model = Product
    template_name = "auth/product_details.html"


class ManageProductsView(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = Product
    template_name = "auth/manage_products.html"

    # def get_queryset(self):
    #     return Product.objects.filter(quantity__gte=1).order_by('-id')

class EditProductsView(SuccessMessageMixin, UpdateView):
    model = Product
    form_class = AddProductForm
    success_message = "Product has been edited successfully!"

    template_name = "auth/edit_product.html"

    def get_success_url(self):
        return reverse("auth:edit_product", kwargs={
            'slug':self.kwargs['slug']
        })

class AddProductView(LoginRequiredMixin, CreateView):
    login_url = '/auth/login'
    form_class = AddProductForm
    model = Product
    template_name = 'auth/add_product.html'

    success_url = reverse_lazy("auth:manage_products")

class ProductDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = '/auth/login'
    model = Product
    success_message = "Product deleted successfully!"

    def get_success_url(self):
        return reverse("auth:manage_products")

class CreateAccountView(SuccessMessageMixin, CreateView):
    model = Accounts
    form_class = AccountCreationForm
    template_name = 'auth/add_customer.html'
    success_message = "Account created successfully!"

    def get_success_url(self):
        return reverse("auth:add_customer")

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data.get('password'))
        form.instance.email = form.cleaned_data.get('email').strip().lower()
        return super().form_valid(form)

class ManageCustomersView(ListView):
    model = Accounts
    template_name = "auth/manage_customer.html"

    def get_queryset(self):
        return Accounts.objects.filter(is_staff=False).order_by('-id')

class AccountDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = '/auth/login'
    model = Accounts
    success_message = "Account deleted successfully!"

    def get_success_url(self):
        return reverse("auth:manage_customer")

class CreateAdminAccountView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = '/auth/login'

    model = Accounts
    form_class = AccountCreationForm
    template_name = 'auth/add_admin.html'
    success_message = "Account created successfully!"

    def get_success_url(self):
        return reverse("auth:add_admin")

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data.get('password'))
        form.instance.email = form.cleaned_data.get('email').strip().lower()
        form.instance.is_staff = True
        return super().form_valid(form)

class ManageAdminView(LoginRequiredMixin, ListView):
    login_url = '/auth/login'

    model = Accounts
    template_name = "auth/manage_admin.html"

    def get_queryset(self):
        return Accounts.objects.filter(is_staff=True).order_by('-id')

class DeleteAdmin(AccountDeleteView):
    login_url = '/auth/login'

    def __init__(self, *args):
        super(AccountDeleteView, self).__init__(*args)

    def get_success_url(self):
        return reverse("auth:manage_admin")

class OrderSummaryView(LoginRequiredMixin, View):
    login_url = '/auth/login'

    def get(self, request):
        try:
            order = Order.objects.get(user=request.user, ordered=False)

            context = {
                'orders': order
            }


            for order in order.product.all():
                product = Product.objects.get(slug=order.product.slug)


                if product.quantity < 1:

                    order_item = OrderItem.objects.filter(user=request.user, completed=False, product=product)[0]

                    order_item.delete()

                    messages.error(request, f'{product.title} you ordered for is now out of stock and has been removed from cart!')
                    return render(request, 'auth/order_summary.html', context)

        except ObjectDoesNotExist:
            messages.error(request, 'You do not have an active order')
            return redirect('auth:all_products')
        return render(request, 'auth/order_summary.html', context)

def stripe_payment(email, fullname, amount, source):
    try:
        customer = stripe.Customer.create(
            email = email,
            name = fullname,
            description = 'Goods payment',
            source = source
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount=amount * 100,
            currency='NGN',
            description='Goods payment',
        )
        return charge
    except stripe.error.CardError as e:
        messages.error(request, f'{e.user_message}')
    except stripe.error.RateLimitError as e:
        messages.error(request, f'Too many request has been made quickly')
    except stripe.error.InvalidRequestError as e:
        messages.error(request, f'Invalid parameters supplied')
    except stripe.error.AuthenticationError as e:
        messages.error(request, f'Authentication with stripe failed')
    except stripe.error.APIConnectionError as e:
        messages.error(request, f'Network problem try again')
    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        messages.error(request, f'Something went wrong, you were not charged please try again!')
    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        messages.error(request, f'Something serious went wrong, we have been notified!')

class CheckOutView(LoginRequiredMixin, View):
    login_url = '/auth/login'

    def get(self, request):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            form = BillingForm(instance=request.user)
            context = {
                'orders': order,
                'form': form
            }
        except ObjectDoesNotExist:
            messages.error(request, 'You do not have an active order')
            return redirect('auth:all_products')
        return render(request, 'auth/checkout.html', context)

    def post(self, request):
        form = BillingForm(request.POST, instance=request.user)

        if form.is_valid():
            order = Order.objects.get(user=request.user, ordered=False)
            details = form.save(commit=False)

            email = details.email
            fullname = details.fullname
            amount = round(order.get_total())
            address = request.POST.get('address')

            if amount > 999999.99:
                messages.warning(request, 'Amount cannot be greater than 99999999₦ on a Test payment')
                return render(request, 'auth/checkout.html', {'form':form})

            source = request.POST.get('stripeToken')
            charge = stripe_payment(email, fullname, amount, source)
            if charge:
                pass
            else:
                return render(request, 'auth/checkout.html', {'form':form})

            # CREATE the payment and billing
            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                # stripe_charge_id='STRIPE_test',
                stripe_charge_id=charge['id'],
            )
            billing = BillingInformation.objects.create(
                user=request.user,
                address=address,
            )
            # ASSIGN payment, billing to the order and set ordered to be true
            order.payment = payment
            order.user = request.user
            order.ordered = True
            order.billing = billing
            order.save()

            # SUBTRACT quantity from product
            for order in order.product.all():
                product = Product.objects.get(slug=order.product.slug)
                product.quantity -= order.quantity
                product.save()

            # ASSIGN orderItem to user
            order_item = OrderItem.objects.filter(user=request.user)
            for item in order_item:
                item.user = request.user
                item.completed = True
                item.save()

            # If payment successful
            messages.success(request, 'Order was successful!')
            return redirect('auth:dashboard')

        return render(request, 'auth/checkout.html', {'form':form})

class MyOrderView(LoginRequiredMixin, ListView):
    login_url = '/auth/login'
    model = Order
    template_name = "auth/my_orders.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.filter(ordered=True).order_by('-id')
        return Order.objects.filter(user=self.request.user, ordered=True).order_by('-id')

class MyOrderDetailView(LoginRequiredMixin, DetailView):
    login_url = '/auth/login'
    model = Order
    template_name = "auth/my_order_details.html"

def confirm_delivery(request):
    try:
        key = request.POST.get('key')
        order = Order.objects.get(pk=key)
        if 'do' in request.POST:
            order.delivered = True
            messages.success(request, 'Delivery of item confirmed!')
        else:
            order.delivered = False
            messages.success(request, 'Change of delivery status successful!')
        order.save()
        return redirect('auth:my_orders')
    except :
        messages.error(request, 'Order not found!')
        return redirect('auth:my_orders')

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("Utf-8")), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class ViewPDF(LoginRequiredMixin, View):
    login_url = '/auth/login'
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(pk=kwargs['order_id'])
            context = {'order':order}
            pdf = render_to_pdf('auth/receipt.html', context)
            return render(request, 'auth/receipt.html', context)
        except ObjectDoesNotExist:
            messages.info(request, 'Unable to generate invoice!!')
            return redirect('auth:my_orders')

