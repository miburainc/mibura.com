from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

# Create your models here.
class Job(models.Model):
	title = models.CharField(max_length=128)
	position = models.CharField(max_length=64)
	location = models.CharField(max_length=128)
	country = models.CharField(max_length=64)

	description = models.TextField()
	responsibilities = models.TextField()
	requirements = models.TextField()
	qualifications = models.TextField()

	benefits = models.CharField(max_length=128, blank=True)
	salary = models.CharField(max_length=64, blank=True)
	job_type = models.CharField(max_length=64, blank=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	slug = models.SlugField()

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title + " " + self.location + " " + self.country)
		super(Job, self).save(*args, **kwargs)


# Application

class Application(models.Model):
	job = models.ForeignKey(Job)

	name = models.CharField(max_length=128)
	location = models.CharField(max_length=128)
	country = models.CharField(max_length=64)

	cover = models.TextField()
	comments = models.CharField(max_length=500, blank=True)

	resume = models.FileField(upload_to='resumes/', null=True, blank=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name