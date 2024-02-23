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

    CreateAccountView,
    ManageCustomersView,
    AccountDeleteView,
    ProductDeleteView,

    CreateAdminAccountView,
    ManageAdminView,
    DeleteAdmin,

    OrderSummaryView,
    CheckOutView,
    MyOrderView,
    MyOrderDetailView,
    confirm_delivery,

    ViewPDF,
)

app_name = 'auth'

urlpatterns = [
    # Dashboard
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('profile/<int:user_id>', ProfileView.as_view(), name='profile'),

    # ACCOUNTS
    path('add_customer', CreateAccountView.as_view(), name='add_customer'),
    path('manage_customer', ManageCustomersView.as_view(), name='manage_customer'),
    path('delete_customer/<pk>', AccountDeleteView.as_view(), name='delete_customer'),

    # ADMIN
    path('add_admin', CreateAdminAccountView.as_view(), name='add_admin'),
    path('manage_admin', ManageAdminView.as_view(), name='manage_admin'),
    path('delete_admin/<pk>', DeleteAdmin.as_view(), name='delete_admin'),

    # ORDER
    path('order_summary', OrderSummaryView.as_view(), name='order_summary'),
    path('checkout', CheckOutView.as_view(), name='checkout'),
    path('my_orders', MyOrderView.as_view(), name='my_orders'),
    path('my_orders_details/<pk>', MyOrderDetailView.as_view(), name='my_orders_details'),
    path('confirm_delivery', confirm_delivery, name='confirm_delivery'),

    # Receipt
    path('receipt/<int:order_id>', ViewPDF.as_view(), name='receipt'),

    # PRODUCT
    path('all_products', AllProductsListView.as_view(), name='all_products'),
    path('product_details/<slug>', ProductDetailListView.as_view()  , name='product_details'),
    path('manage_products', ManageProductsView.as_view(), name='manage_products'),
    path('edit_product/<slug>', EditProductsView.as_view(), name='edit_product'),
    path('delete_product/<slug>', ProductDeleteView.as_view(), name='delete_product'),
    path('add_product', AddProductView.as_view(), name='add_product'),

    # AUTH
    path('register', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

]