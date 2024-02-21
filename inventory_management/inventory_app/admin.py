from django.contrib import admin
from .models import Inventory, UserRole, UserRecord

# Register your models here.

admin.site.register(Inventory)
admin.site.register(UserRole)
admin.site.register(UserRecord)