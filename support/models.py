from django.conf import settings
from django.db import models

from datetime import datetime, timedelta
from pytz import timezone


PLAN_CHOICES = (
	("silver", "Silver"),
	("gold", "Gold"),
	("black", "Black"),
)

PRODUCT_CATEGORIES = (
	("servers", "Servers"),
	("storage", "Storage Appliances"),
	("network", "Networking"),
	("appliances", "Appliances"),
)

class Cloud(models.Model):
	name = models.CharField(max_length=128)
	website = models.CharField(max_length=128)
	price_modifier = models.FloatField(default=0.0)

	color = models.CharField(max_length=64, blank=True)
	image = models.ImageField(upload_to='images/cloud/', blank=True)

	def __str__(self):
		return self.name


class Product(models.Model):
	brand = models.CharField(max_length=128)
	model = models.CharField(max_length=128)
	sku = models.CharField(max_length=128)

	category = models.CharField(max_length=32, choices=PRODUCT_CATEGORIES)
	price_silver = models.FloatField(default=0.0)
	price_gold = models.FloatField(default=0.0)
	price_black = models.FloatField(default=0.0)

	with_cloud = models.FloatField(default=0.0)

	release = models.DateField(blank=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.brand + " : " + self.model


class Client(models.Model):
	first_name = models.CharField(max_length=32)
	last_name = models.CharField(max_length=32)
	email = models.CharField(max_length=128)
	phone = models.CharField(max_length=32)
	company = models.CharField(max_length=128)

	street = models.CharField(max_length=64)
	street2 = models.CharField(max_length=64, blank=True)
	city = models.CharField(max_length=64)
	state = models.CharField(max_length=64)
	country = models.CharField(max_length=64)
	zipcode = models.CharField(max_length=64)
	
	def get_full_name(self):
		return self.first_name + " " + self.last_name

	def __str__(self):
		return self.get_full_name()

class ClientProduct(models.Model):
	client = models.ForeignKey(Client)
	product = models.ForeignKey(Product, blank=True, null=True)

	brand = models.CharField(max_length=64, blank=True)
	model = models.CharField(max_length=64, blank=True)

	serial_number = models.CharField(max_length=128, blank=True)
	device_age = models.IntegerField(default=0)
	additional_info = models.TextField(blank=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.product) if self.product else self.brand + " " + self.model

class Subscription(models.Model):
	client = models.ForeignKey(Client)
	plan = models.CharField(max_length=32, choices=PLAN_CHOICES)
	products = models.ManyToManyField(ClientProduct)

	length = models.FloatField(default=1)
	price = models.FloatField(default=0.0)
	discount_code = models.CharField(max_length=64, blank=True)

	date_begin = models.DateTimeField(blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def get_expiration(self):
		return self.date_begin + timedelta(days=self.length*365)

	def __str__(self):
		return self.client.get_full_name() + ": " + self.plan

class Cart(models.Model):
	email = models.CharField(max_length=128)
	client = models.ForeignKey(Client)
	products = models.ManyToManyField(ClientProduct)

	plan = models.CharField(max_length=32, choices=PLAN_CHOICES)

	reference = models.CharField(max_length=128) # Reference code for client to use

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.client.get_full_name() + " Cart " + str(self.date_created)
