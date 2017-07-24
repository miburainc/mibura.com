from django.contrib import admin

from .models import *

# Register your models here.

class ClientAdmin(admin.ModelAdmin):
	fields = ['name', 'email', 'company']

admin.site.register(Client, ClientAdmin)

class ProductAdmin(admin.ModelAdmin):
	list_display = ['brand', 'model', 'sku']

admin.site.register(Product, ProductAdmin)

class CartAdmin(admin.ModelAdmin):
	list_display = ['client', 'reference', 'date_created', 'date_updated']

admin.site.register(Cart, CartAdmin)

class ClientProductAdmin(admin.ModelAdmin):
	list_display = ['client', 'product', 'serial_number']

admin.site.register(ClientProduct, ClientProductAdmin)

class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ['client', 'plan', 'price', 'date_created', 'date_updated']

admin.site.register(Subscription, SubscriptionAdmin)

class CloudAdmin(admin.ModelAdmin):
	list_display = ['name', 'website', 'price_modifier',]

admin.site.register(Cloud, CloudAdmin)