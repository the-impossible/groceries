# My django imports
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

# My app imports
from OBMS_auth.forms import AccountCreationForm, EditAccountCreationForm
from OBMS_auth.models import Accounts
from OBMS_basics.models import Product

# Create your views here.
class DashboardView(View):
    def get(self, request):
        return render(request,'auth/dashboard.html')

class RegisterView(View):
    def get(self, request):
        context = {
            'form': AccountCreationForm()
        }
        return render(request,'auth/register.html', context)

    def post(self, request):
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.set_password(form.password)
            form.save()
            messages.success(request, 'Account created successfully, you can now login!')
            return redirect('auth:login')
        else:
            messages.error(request, 'Error creating account!')
            context = {
                'form': form,
            }
        return render(request,'auth/register.html', context)

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        email = request.POST.get('email').strip()
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
    paginate_by = 10
    template_name = "auth/all_products.html"

class ProductDetailListView(DetailView):
    model = Product
    template_name = "auth/product_details.html"


