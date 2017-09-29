from django.contrib import admin

from .models import *

# Register your models here.

class StripeClientAdmin(admin.ModelAdmin):
	list_display = ['client', 'customer_id', 'bank_id', 'bank_verified']

admin.site.register(StripeClient, StripeClientAdmin)

class PaymentAdmin(admin.ModelAdmin):
	list_display = ['client', 'cart', 'payment_type', 'token', 'amount', 'completed']

admin.site.register(Payment, PaymentAdmin)