from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Inventory(models.Model):
    product_id = models.CharField(max_length=50)
    product_name = models.CharField(max_length=100)
    vendor = models.CharField(max_length=100)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    batch_num = models.CharField(max_length=50)
    batch_date = models.DateField()
    quantity = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=(("Approved", "Approved"), ("Pending", "Pending")))
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.product_name

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=(("Department Manager", "Department Manager"), ("Store Manager", "Store Manager")))

class UserRecord(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username