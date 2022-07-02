# My django imports
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
# My app imports
from OBMS_auth.forms import AccountCreationForm, EditAccountCreationForm, BillingForm
from OBMS_auth.models import Accounts
from OBMS_basics.models import Product, Order, BillingInformation, Payment, OrderItem
import stripe
stripe.api_key = "sk_test_51L5Xs6GCAqCizi1RncjTC84yc0J7jaecLFB5gj07ZDNWCREFyEylsunXTltlQleL3lWzEcLsqIFCInvn6wGYu2Xa00cIHRZjMz"

# Create your views here.
class DashboardView(View):
    def get(self, request):
        return render(request,'auth/dashboard.html')

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
        jump_to =  request.POST.get('next', None)
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')

        if email and password:
            # Authenticate user
            user = authenticate(request, email=email, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'You are now signed in {user.get_name()}')
                    if jump_to == 'None':
                        return redirect('auth:dashboard')
                    return redirect(f"auth:{jump_to.split('/')[-1]}")

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

class ProfileView(View):
    def get(self, request, user_id):
        user = get_object_or_404(Accounts, id=user_id)
        form = EditAccountCreationForm(instance=user)
        context = {
            'form':form,
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

class AllProductsListView(ListView):
    model = Product
    paginate_by = 8
    template_name = "auth/all_products.html"
    ordering = ['-id']

class ProductDetailListView(DetailView):
    model = Product
    template_name = "auth/product_details.html"

class ManageProductsView(ListView):
    model = Product
    template_name = "auth/manage_products.html"

    def get_queryset(self):
        return Product.objects.filter(quantity__gte=1).order_by('-id')

class EditProductsView(SuccessMessageMixin, UpdateView):
    model = Product
    success_message = "Product has been edited successfully!"
    fields = [
        "title",
        "price",
        "quantity",
        "description",
        "image",
    ]
    template_name = "auth/edit_product.html"

    def get_success_url(self):
        return reverse("auth:edit_product", kwargs={
            'slug':self.kwargs['slug']
        })

class AddProductView(CreateView):
    model = Product
    fields = [
        "title",
        "price",
        "quantity",
        "slug",
        "description",
        "image",
    ]
    template_name = 'auth/add_product.html'

    success_url = reverse_lazy("auth:manage_products")

class ProductDeleteView(SuccessMessageMixin, DeleteView):
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

class AccountDeleteView(SuccessMessageMixin, DeleteView):
    model = Accounts
    success_message = "Account deleted successfully!"

    def get_success_url(self):
        return reverse("auth:manage_customer")

class CreateAdminAccountView(SuccessMessageMixin, CreateView):
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

class ManageAdminView(ListView):
    model = Accounts
    template_name = "auth/manage_admin.html"

    def get_queryset(self):
        return Accounts.objects.filter(is_staff=True).order_by('-id')

class DeleteAdmin(AccountDeleteView):
    def __init__(self, *args):
        super(AccountDeleteView, self).__init__(*args)

    def get_success_url(self):
        return reverse("auth:manage_admin")

class OrderSummaryView(View):
    def get(self, request):
        try:
            order = Order.objects.get(session_id=request.session['nonuser'], ordered=False)
            context = {
                'orders': order
            }
        except ObjectDoesNotExist:
            messages.error(request, 'You do not have an active order')
            return redirect('auth:all_products')
        return render(request, 'auth/order_summary.html', context)

def stripe_payment(email, fullname, amount, source):
    try:
        customer = stripe.Customer.create(
            email = email,
            name = fullname,
            description = 'OBMS Goods payment',
            source = source
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount=amount * 100,
            currency='NGN',
            description='OBMS Goods payment',
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
            order = Order.objects.get(session_id=request.session['nonuser'], ordered=False)
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
            order = Order.objects.get(session_id=request.session['nonuser'], ordered=False)
            details = form.save(commit=False)

            email = details.email
            fullname = details.fullname
            amount = round(order.get_total())
            address = request.POST.get('address')

            if amount > 999999.99:
                messages.warning(request, 'Amount cannot be greater than 99999999₦ on a Test payment')
                return render(request, 'auth/checkout.html', {'form':form})

            # source = request.POST.get('stripeToken')
            # charge = stripe_payment(email, fullname, amount, source)
            # if charge:
            #     pass
            # else:
            #     return render(request, 'auth/checkout.html', {'form':form})

            # CREATE the payment and billing
            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                stripe_charge_id='STRIPE_test',
                # stripe_charge_id=charge['id]',
                session_id=request.session['nonuser']
            )
            billing = BillingInformation.objects.create(
                user=request.user,
                address=address,
                session_id=request.session['nonuser']
            )
            # ASSIGN payment, billing to the order and set ordered to be true
            order.payment = payment
            order.user = request.user
            order.ordered = True
            order.billing = billing
            order.save()

            # SUBTRACT quantity from product
            print('ORDER', order.product.all())
            for order in order.product.all():
                product = Product.objects.get(slug=order.product.slug)
                product.quantity -= order.quantity
                product.save()

            # ASSIGN orderItem to user
            order_item = OrderItem.objects.filter(session_id=request.session['nonuser'])
            for item in order_item:
                item.user = request.user
                item.completed = True
                item.save()

            # If payment successful
            messages.success(request, 'Order was successful!')
            return redirect('auth:dashboard')

        return render(request, 'auth/checkout.html', {'form':form})
