# My django imports
from django.urls import path

# My app imports
from OBMS_auth.views import (
    DashboardView,
    RegisterView,
    LoginView,
    ProfileView,
)

app_name = 'auth'

urlpatterns = [
    # Dashboard
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('profile', ProfileView.as_view(), name='profile'),

    # AUTH
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),

]