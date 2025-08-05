from django.contrib import admin
from . models import Shelf, Item, Profile, CustomUser, CartItem, Order
# Register your models here.

@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ('shelf_number',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'shelf', "item_price")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone_number')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id',)