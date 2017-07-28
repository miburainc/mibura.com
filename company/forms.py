from django.utils.translation import ugettext as _
from django import forms
from django.conf import settings



from .models import Application

class JobApplicationForm(forms.ModelForm):
	class Meta:
		model = Application
		fields = ['name', 'job', 'location', 'country', 'cover', 'resume', 'comments']

	def __init__(self, *args, **kwargs):
		super(JobApplicationForm, self).__init__(*args, **kwargs)
		self.fields['resume'].required = True

	def clean_resume(self):
		print("clean_file() in form")
		resume = self.cleaned_data.get('resume')
		print(resume)
		if resume:
			file_type = resume.content_type
			print(file_type)

			if len(resume.name.split('.')) == 1:
				print("File type is not supported")
				raise forms.ValidationError(_('File type is not supported'), code='invalid')

			if file_type in settings.TASK_UPLOAD_FILE_TYPES:
				if resume._size > settings.TASK_UPLOAD_FILE_MAX_SIZE:
					print("Please keep filesize under")
					raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.TASK_UPLOAD_FILE_MAX_SIZE), filesizeformat(file._size)))
			else:
				print("File type is not supported")
				raise forms.ValidationError(_('File type is not supported'), code='invalid')
		return resume
	# def clean_name(self):
	# 	print("clean_name() in form")
	# 	name = self.cleaned_data['name']
	# 	if not name:
	# 		print("Not cleaned_data[name]")
	# 		raise forms.ValidationError('Please enter your name in text box.')
	# 	return name