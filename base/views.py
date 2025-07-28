from django.shortcuts import render, redirect
from . models import Shelf, Item
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile, Item, Cart, CartItem
from .forms import CustomUserCreationForm

# authenticate, login, logout: Handle user authentication.
# UserCreationForm: Provides a form for creating new users based on CustomUser.
# .models: Imports your defined models for database operations.

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
        form = UserCreationForm()
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
    return render(request, 'base/edit_profile.html', {'form': form})
    
def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart = request.user.cart
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'base/cart.html', {'cart_items':cart_items})

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
    cart_item.delete()
    return redirect('cart')

