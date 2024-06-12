from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
import datetime
import os
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


#models.py:
class CustomUser(AbstractUser):
    # Add any additional fields you need
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    class Meta:
        unique_together = ('username', 'email')

CustomUser = get_user_model()

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50,default='')
    phone_number = models.CharField(max_length=15,default='')
    home = models.CharField(max_length=55, blank=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    class Meta:
        unique_together = ('user', 'street', 'city', 'state', 'zip_code')

class Seller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='seller_profile')
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False) 


    def __str__(self):
        return self.company_name
    def __str__(self):
        return self.user.username
    
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def _str_(self):
        return self.user.username
    

    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Product(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=150)
    price = models.FloatField()
    description = models.CharField(max_length=300)
    description_2 = models.CharField(max_length=300, blank=True, null=True)
    description_3 = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to='media/uploads')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)  # Linking Product with Seller
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reorder_level = models.PositiveIntegerField(default=0)

    # Add quantity fields for each size variant
    quantity_S = models.PositiveIntegerField(default=0)
    quantity_M = models.PositiveIntegerField(default=0)
    quantity_L = models.PositiveIntegerField(default=0)
    quantity_XL = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def total_product_price(self):
        return self.price * (self.quantity_S + self.quantity_M + self.quantity_L + self.quantity_XL)

    def is_out_of_stock(self):
        return self.quantity_S == 0 and self.quantity_M == 0 and self.quantity_L == 0 and self.quantity_XL == 0


from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Models

class ShippingDetails(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"Shipping details for {self.user.username}"


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.size})"

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping_details = models.ForeignKey(ShippingDetails, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField()
    products = models.ManyToManyField(Product, through='OrderItem')

    

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=10, blank=True, null=True)
    price = models.FloatField()

    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.size})"

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.size})"

class OrderStatus(models.Model):
    STATUS_CHOICES = (
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    pstatus = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    @property
    def total_cost(self):
        return self.product.price * self.quantity
