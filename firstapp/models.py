from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# CustomUser Model
class CustomUser(AbstractUser):
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    hobbies = models.TextField(blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    document_upload = models.FileField(upload_to='documents/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    language = models.CharField(max_length=20, blank=True, null=True)

    # Adding related_name to avoid clashes
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    def __str__(self):
        return self.username


# OTP Model
class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_code = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.username} - Code: {self.otp_code}"


# Product Model for Super Admin
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"



from django.db import models
from django.conf import settings  # Import settings to use AUTH_USER_MODEL
from django.db.models import CASCADE

class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use the custom user model if defined
        on_delete=CASCADE,
        related_name='cart_items'
    )
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} for {self.user.username}"

# Like model
from django.db import models
from django.conf import settings
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Updated
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.user} liked {self.product}"

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Updated
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} commented on {self.product}: {self.content[:20]}"