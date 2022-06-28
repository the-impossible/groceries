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
    ManageProductsView,
    EditProductsView,
    AddProductView,
    delete_product,
    CreateAccountView
)

app_name = 'auth'

urlpatterns = [
    # Dashboard
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('profile/<int:user_id>', ProfileView.as_view(), name='profile'),

    # ACCOUNTS
    path('add_customer', CreateAccountView.as_view(), name='add_customer'),

    # PRODUCT
    path('all_products', AllProductsListView.as_view(), name='all_products'),
    path('product_details/<slug>', ProductDetailListView.as_view(), name='product_details'),
    path('manage_products', ManageProductsView.as_view(), name='manage_products'),
    path('edit_product/<slug>', EditProductsView.as_view(), name='edit_product'),
    path('add_product', AddProductView.as_view(), name='add_product'),
    path('delete_product', delete_product, name='delete_product'),

    # AUTH
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

]