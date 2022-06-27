# My django imports
from django.urls import path

# My app imports
from OBMS_auth.views import (
    RegisterView,
    LoginView,
    LogoutView,

    DashboardView,
    ProfileView,
    AllProductsListView,
    ProductDetailListView,
)

app_name = 'auth'

urlpatterns = [
    # Dashboard
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('profile/<int:user_id>', ProfileView.as_view(), name='profile'),
    # PRODUCT
    path('all_products', AllProductsListView.as_view(), name='all_products'),
    path('product_details/<slug>', ProductDetailListView.as_view(), name='product_details'),

    # AUTH
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

]