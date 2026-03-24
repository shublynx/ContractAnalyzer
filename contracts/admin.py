from django.contrib import admin

# Register your models here.
from .models import User, Contract

admin.site.register(User)
admin.site.register(Contract)