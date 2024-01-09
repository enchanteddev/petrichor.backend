from django.contrib import admin

from commerce.models import Address, Item, PaymentTable

# Register your models here.

admin.site.register(Item)
admin.site.register(PaymentTable)
admin.site.register(Address)