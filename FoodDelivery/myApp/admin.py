from django.contrib import admin

from .models import Cart, Listings, Stores

# Register your models here.

admin.site.register(Stores)
admin.site.register(Listings)

admin.site.register(Cart)