from django.contrib import admin

# Register your models here.
from .models import User, Contract, ContractChunk

admin.site.register(User)
admin.site.register(Contract)
admin.site.register(ContractChunk)
