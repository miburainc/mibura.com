from django.contrib import admin

from .models import *

# Register your models here.

class ClientAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'email', 'company']

admin.site.register(Client, ClientAdmin)

class ProductAdmin(admin.ModelAdmin):
	search_fields = ['brand', 'model', 'sku']
	list_filter = ['brand', 'category']
	list_display = ['brand', 'model', 'category', 'sku', 'release']

admin.site.register(Product, ProductAdmin)

class CartAdmin(admin.ModelAdmin):
	search_fields = ['reference']
	list_display = ['client', 'reference', 'date_created', 'date_updated']

admin.site.register(Cart, CartAdmin)

class ClientProductAdmin(admin.ModelAdmin):
	search_fields = ['product', 'brand', 'model', 'client']
	list_filter = ['client', 'product', 'brand']
	list_display = ['client', 'product', 'brand', 'model', 'serial_number']

admin.site.register(ClientProduct, ClientProductAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ['client', 'plan', 'price', 'date_begin', 'date_created', 'date_updated']

admin.site.register(Subscription, SubscriptionAdmin)

class CloudAdmin(admin.ModelAdmin):
	list_display = ['name', 'website', 'price_modifier',]

admin.site.register(Cloud, CloudAdmin)