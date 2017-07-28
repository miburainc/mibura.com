from django.contrib import admin

from .models import Job, Application

# Register your models here.
class JobAdmin(admin.ModelAdmin):
	list_filter = ['location', 'country']
	list_display = ['title', 'position', 'location', 'date_created']

admin.site.register(Job, JobAdmin)

class ApplicationAdmin(admin.ModelAdmin):
	list_filter = ['name', 'location', 'country']
	list_display = ['name', 'job', 'location', 'date_created']

admin.site.register(Application, ApplicationAdmin)