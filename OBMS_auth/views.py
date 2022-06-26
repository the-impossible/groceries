# My django imports
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

# My app imports
from OBMS_auth.forms import AccountCreationForm

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

class ProfileView(View):
    def get(self, request):
        return render(request,'auth/profile.html')