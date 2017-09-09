from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import Job
from .forms import JobApplicationForm

# Create your views here.
def index(request):
	context = {}
	jobs = Job.objects.all()
	context['jobs'] = jobs
	return render(request, 'company/index.html', context)

def job2(request, slug):
	context = {}
	job = Job.objects.get(slug=slug)
	context['job'] = job
	return render(request, 'company/job.html', context)

def job(request, slug):
	context = {}
	job = Job.objects.get(slug=slug)
	context['job'] = job
	context['form'] = JobApplicationForm(request.POST or None, request.FILES or None)
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = JobApplicationForm(request.POST, request.FILES)
		context['form'] = form
		# check whether it's valid:
		print("Received post request")
		if form.is_valid():
			print("Form Valid")
			obj = form.save(commit=False)
			# process the data in form.cleaned_data as required
			obj.name = form.cleaned_data['name']
			obj.location = form.cleaned_data['location']
			obj.country = form.cleaned_data['country']
			obj.cover = form.cleaned_data['cover']
			obj.comments = form.cleaned_data['comments']

			obj.save()
			# redirect to a new URL:
			messages.success(request, "Application Submitted Successfully!")
			messages.success(request, "We will get back to you shortly.")
			return HttpResponseRedirect(reverse('company-thanks'))
		else:
			print("Form invalid")
	# if a GET (or any other method) we'll create a blank form
	else:
		form = JobApplicationForm(initial={'job': job.pk})

		context['form'] = form

	return render(request, 'company/job.html', context)


from django.core.mail import send_mail

# if form.is_valid():
# 	subject = form.cleaned_data['subject']
# 	message = form.cleaned_data['message']
# 	sender = form.cleaned_data['sender']
# 	cc_myself = form.cleaned_data['cc_myself']

# 	recipients = ['info@example.com']
# 	if cc_myself:
# 		recipients.append(sender)

# 	send_mail(subject, message, sender, recipients)
# 	return HttpResponseRedirect('/thanks/')