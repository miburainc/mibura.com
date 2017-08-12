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
	list_display = ['name', 'website', 'price_multiplier',]

admin.site.register(Cloud, CloudAdmin)

class ProductCategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'yearly_tax', 'category_code', 'price_multiplier',]

admin.site.register(ProductCategory, ProductCategoryAdmin)

class PlanAdmin(admin.ModelAdmin):
	list_display = ['name', 'short_name', 'price', 'color',]

admin.site.register(Plan, PlanAdmin)

class DiscountAdmin(admin.ModelAdmin):
	list_display = ['year_threshold', 'discount_percent']

admin.site.register(Discount, DiscountAdmin)