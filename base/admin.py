from django.contrib import admin
from . models import Shelf, Item, Profile, CustomUser
# Register your models here.

@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ('shelf_number',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'shelf')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone_number')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email',)