from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . models import Shelf, Item
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile, Item, Cart, CartItem, Order, OrderItem
from .forms import CustomUserCreationForm
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404
from django.http import JsonResponse

# authenticate, login, logout: Handle user authentication.
# UserCreationForm: Provides a form for creating new users based on CustomUser.
# .models: Imports your defined models for database operations.

def superuser_required(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(superuser_required, login_url='/access-denied/')
def operation_form_view(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    context = {
        'order': order,
        'user': order.user,  # Assuming Order has a ForeignKey to CustomUser
    }
    return render(request, 'base/operation_form.html', context)

@user_passes_test(superuser_required, login_url='/access-denied/')
def order_list_view(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'base/order_list.html', {'orders': orders})

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone_number']

def home(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    items = Item.objects.all()
    return render(request, 'base/home.html', {'items': items})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            Cart.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    context = {'form':form}
    return render(request, 'base/register.html', context)


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        if not email or not password:
            return render(request, 'base/login.html', {'error': 'Email ve şifre giriniz.'})
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'base/login.html', {'error': 'Geçersiz email veya şifre !'})
    return render(request, 'base/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    profile = request.user.profile
    return render(request, 'base/profile.html', {'profile': profile})

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:    
        form = ProfileEditForm(instance=profile)
    context = {
        'form': form,
        'profile': profile
        }
    return render(request, 'base/edit_profile.html', context)
    
def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart = request.user.cart
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = 0
    for item in cart_items:
        total_price += int(item.quantity * item.item.item_price)
    # total_price = sum(item.item.item_price * item.quantity for item in cart_items)
    context = {'cart_items':cart_items, 'total_price': total_price}
    return render(request, 'base/cart.html', context)

def add_to_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')
    cart = request.user.cart
    item = Item.objects.get(id=item_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('home')

def remove_from_cart(request, cart_item_id):
    if not request.user.is_authenticated:
        return redirect('login')
    cart_item = CartItem.objects.get(id=cart_item_id, cart=request.user.cart)
    cart_item.quantity -= 1
    cart_item.save()
    if cart_item.quantity == 0:
        cart_item.delete()
    return redirect('cart')

# def create_operation_form(request):
#     user = request.user
#     order = Order.objects.filter(user=user).order_by('-order_date').first()
#     context = {
#         'order': order,
#         'user': user,
#     }
#     return render(request, 'base/operation_form.html', context)

@login_required
def create_order(request):
    try:
        profile = request.user.profile
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        
        if not cart_items:
            return JsonResponse({'status': 'error', 'message': 'Cart is empty'}, status=400)

        # Create a new order
        order = Order.objects.create(user=request.user)

        # Move cart items to order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                quantity=cart_item.quantity,
            )

        # Clear the cart after creating the order
        cart_items.delete()

        return JsonResponse({'status': 'success', 'message': 'Order created successfully'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    # try:
    #     profile = request.user.profile
    #     cart = Cart.objects.get(user=request.user)
    #     cart_items = CartItem.objects.filter(cart=cart)
        
    #     if not cart_items:
    #         return render(request, 'base/home.html')

    #     # Create a new order
    #     order = Order.objects.create(user=request.user)

    #     # Move cart items to order items
    #     for cart_item in cart_items:
    #         OrderItem.objects.create(
    #             order=order,
    #             item=cart_item.item,
    #             quantity=cart_item.quantity,
    #         )

    #     # Clear the cart after creating the order
    #     cart_items.delete()

    #     context = {
    #         'profile': profile,
    #         'order': order,
    #         'user': request.user,
    #     }

    #     return render(request, 'base/operation_form.html', context)

    # except Cart.DoesNotExist:
    #     return render(request, 'base/home.html')