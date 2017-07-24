from django.shortcuts import render

# Create your views here.
# Create your views here.
def index(request):
	"""
	View function for home page of site.
	"""
    
	# Render the HTML template index.html with the data in the context variable
	return render(
		request,
		'staffing/index.html',
	)