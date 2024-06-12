# urls.py

from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views
from django.urls import path, include



urlpatterns = [
    path('',views.home,name='home'),
    path('search/', views.search_results, name='search_results'),
    path('customer/signup/', customer_signup, name='customer_signup'),
    path('customer/login/', customer_login, name='customer_login'),
    path('seller/signup/', seller_signup, name='seller_signup'),
    path('seller/login/', seller_login, name='seller_login'),
    path('seller/dashboard/', seller_dashboard, name='seller_dashboard'),
    path('seller/profile/', views.seller_profile, name='seller_profile'), 
    path('seller/profile/edit/', views.edit_seller_profile, name='edit_seller_profile'),
 # Seller dashboard
    path('logout/', logout_view, name='logout'),






    
    path('a/',views.hom,name='hom'),




    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path('addproduct/',views.product_create,name='product_create'),
    path('categories/', views.category_list, name='category_list'),
    
    path('editproduct/<int:product_id>/', views.product_update, name='product_update'),
    path('view/',views.view,name='view'),
    path('deleteproduct/<int:product_id>/', views.product_delete, name='product_delete'),

    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('delete_from_cart/<int:cart_item_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('increase_quantity/<int:cart_item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:cart_item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
   
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),

    path('order-history/', order_history, name='order_history'),



    # path('order/<int:order_id>/', views.order_details, name='order_details'),  # Add this line
    # path('order_history/', views.order_history, name='order_history'),
    # path('order-list/', views.order_list, name='order-list'),
    path('list_users/', views.list_users, name='list_users'),
    path('remove_user/<int:user_id>/', views.remove_user, name='remove_user'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/change_status/', views.change_order_status, name='change_order_status'),

    path('profile/', views.view_profile, name='view_profile'),
    path('edit_profile/',views.edit_profile, name='edit_profile'),
    
    # path('profile/', views.view_profile, name='view_profile'),
    # path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('user_order_status/', user_order_status, name='user_order_status'),


    path('add_product/', views.add_product, name='add_product'),
    path('seller/products/', views.seller_products, name='seller_products'),
    path('seller/products/<int:product_id>/update/', views.update_product, name='update_product'),
    path('seller/products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/customers/', views.product_customers, name='product_customers'),

    path('reorder-level-alerts/', views.reorder_level_alerts, name='reorder_level_alerts'),



    path('pending-products/', views.pending_products, name='pending_products'),





    # Update the URL pattern



   path('new_suppliers/', views.new_suppliers, name='new_suppliers'),
   path('approved-sellers/', views.approved_sellers, name='approved_sellers'),
   path('delete-seller/<int:seller_id>/', views.delete_seller, name='delete_seller'),
   path('orderssss/', views.view_orders, name='view_orders'),







    path('seller/orders/', views.seller_order_list, name='seller_order_list'),
    path('seller/order/update/<int:order_item_id>/', views.update_order_status, name='update_order_status'),





    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    

]



