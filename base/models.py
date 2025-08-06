from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from datetime import datetime
# Create your models here.

class Shelf(models.Model):
    shelf_number = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.shelf_number
    
class Item(models.Model):
    item_name = models.CharField(max_length=200, unique=True)
    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)    
    item_image = models.ImageField(null=True, default="color_palette.png")
    item_price = models.IntegerField(default=0)
    def __str__(self):
        return self.item_name
    

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200, null=True)
    surname =  models.CharField(max_length=200, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)

    objects = UserManager()

    def __str__(self):
        return self.email
    
class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.item_name} in {self.cart}"
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
    
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    order_id = models.CharField(max_length=20, unique=True, editable=False)
    order_date = models.DateTimeField(auto_now_add=True)

    @property
    def order_only_date(self):
        return self.order_date.date()

    def save(self, *args, **kwargs):
        if not self.order_id:
            # Generate a unique order ID (e.g., timestamp-based or random)
            self.order_id = f"{datetime.now().strftime('%H%M%S')}"
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Order {self.order_id} by {self.user.email}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} {self.item.item_name} in Order {self.order.order_id}"
 