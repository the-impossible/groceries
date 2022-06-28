# My django imports
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.messages.views import SuccessMessageMixin

# My app imports
from OBMS_auth.forms import AccountCreationForm, EditAccountCreationForm
from OBMS_auth.models import Accounts
from OBMS_basics.models import Product

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
        return render(request, 'auth/login.html')

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
                    if user.is_superuser:
                        return redirect('auth:dashboard')
                    else:
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

def delete_product(request):
    slug = request.POST.get('delete')
    product = get_object_or_404(Product, slug=slug)
    messages.success(request, f'{product.title} has been removed!!')
    product.delete()
    return redirect('auth:manage_products')

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
