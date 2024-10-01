from django.contrib import admin
from .models import Category, Item, Inbound, Outbound

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Inbound)
admin.site.register(Outbound)
