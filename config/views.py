from django.shortcuts import render
from django.http import HttpResponse

import cloudinary

# Create your views here.

def index(request):
	"""
	View function for home page of site.
	"""

	context = {}

	return render(
		request,
		'index.html',
		context
	)

def ssl_verification(request):
	return HttpResponse(open('static/ssl/937697B349ECB0FB31EF5BAE50010670.txt').read())