from django.contrib import admin

from .models import *

# Register your models here.

class FreshbooksAuthAdmin(admin.ModelAdmin):
	list_display = ['code', 'auth', 'refresh', 'expires']

admin.site.register(FreshbooksAuth, FreshbooksAuthAdmin)