from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    # path('operation_form/', views.create_operation_form, name="operation_form"),
    path('create-order/', views.create_order, name='create_order'),
    # path('admin_template/', views.admin_only_view, name='admin_temp'),
    path('orders/', views.order_list_view, name='order_list'),
    path('operation_form/<str:order_id>/', views.operation_form_view, name='operation_form'),
   path('remove_order_form/<str:order_id>/', views.remove_order_form, name='remove_form'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)