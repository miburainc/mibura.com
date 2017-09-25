from django.template.defaultfilters import truncatechars
from django.conf import settings
from django.db import models

from datetime import datetime, timedelta
from pytz import timezone

from scripts.sss_pricing import product_price, cloud_price

from freshbooks import clients

PLAN_CHOICES = (
	("silver", "Silver"),
	("gold", "Gold"),
	("black", "Black"),
)

PRODUCT_CATEGORIES = (
	("none", "**No Category**"),
	("servers", "Servers"),
	("storage", "Storage Appliances"),
	("network", "Networking"),
	("appliances", "Appliances"),
)

class Plan(models.Model):
	name = models.CharField(max_length=64)
	short_name = models.CharField(max_length=16)
	color = models.CharField(max_length=12)
	price = models.FloatField(default=0.0)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class Discount(models.Model):
	year_threshold = models.FloatField(default=0.0)
	discount_percent = models.FloatField(default=0.1)

	def __str__(self):
		return "Discount at " + str(self.year_threshold) + " years: " + str(self.discount_percent)


class Cloud(models.Model):
	name = models.CharField(max_length=128)
	website = models.CharField(max_length=128)
	price_multiplier = models.FloatField(default=1.0)

	color = models.CharField(max_length=64, blank=True)
	image = models.ImageField(upload_to='images/cloud/', blank=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class ProductCategory(models.Model):
	name = models.CharField(max_length=32)
	category_code = models.CharField(max_length=32, blank=True)
	price_multiplier = models.FloatField(default=1.0)
	yearly_tax = models.FloatField(default=0.1)

	def __str__(self):
		return self.category_code

	class Meta:
		verbose_name_plural = "Product Categories"

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
	
	freshbooks_id = models.CharField(max_length=32,blank=True)
	dynamicscrm_id = models.CharField(max_length=32,blank=True)
	stripe_customer_id = models.CharField(max_length=32, blank=True)
	stripe_bank_id = models.CharField(max_length=32, blank=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def get_full_name(self):
		return self.first_name + " " + self.last_name

	def get_freshbooks_id(self):
		if not self.freshbooks_id:
			fid = clients.find_client(self.first_name, self.last_name, self.email)
			print(fid)
			if fid:
				print("fid not false:", fid)
				self.freshbooks_id = fid
				self.save()
			else:
				print("fid false:", fid)
				fid = clients.create_client(self.__dict__)
				print("after create_client:", fid)
				self.freshbooks_id = fid
				self.save()
		return self.freshbooks_id

	def get_dynamicscrm_id(self):
		pass

	def __str__(self):
		return self.get_full_name()



class Product(models.Model):
	brand = models.CharField(max_length=128)
	model = models.CharField(max_length=128)
	sku = models.CharField(max_length=128)

	partner_price = models.FloatField(default=0.0)
	retail_price = models.FloatField(default=0.0)

	category = models.ForeignKey(ProductCategory, null=True, blank=True)
	price_silver = models.FloatField(default=1.0)
	price_gold = models.FloatField(default=1.0)
	price_black = models.FloatField(default=1.0)

	release = models.DateField(null=True,blank=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.brand + " : " + self.model

class UnknownProduct(models.Model):
	name = models.CharField(max_length=128)
	serial_number = models.CharField(max_length=128, null=True, blank=True)
	device_age = models.IntegerField(default=0)
	additional_info = models.TextField(blank=True)
	client = models.ForeignKey(Client)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

class CloudAddOn(models.Model):
	cloud = models.ForeignKey(Cloud, null=True)
	cloud_backup_name = models.CharField(max_length=128, default="")
	category = models.CharField(max_length=128)
	sub_category = models.CharField(max_length=128)
	price = models.FloatField(default=0.0)
	is_price_final = models.BooleanField(default=False)


class ClientProduct(models.Model):
	client = models.ForeignKey(Client)
	cloud = models.ForeignKey(Cloud, blank=True, null=True)
	product = models.ForeignKey(Product, blank=True, null=True)
	quantity = models.IntegerField(default=1, blank=True, null=True)

	brand = models.CharField(max_length=64, blank=True) # Take off
	model = models.CharField(max_length=64, blank=True) # take off

	serial_number = models.CharField(max_length=128, null=True, blank=True)
	device_age = models.IntegerField(default=0)
	additional_info = models.TextField(blank=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.product) if self.product else self.brand + " " + self.model


class Cart(models.Model):
	email = models.CharField(max_length=128)
	client = models.ForeignKey(Client)
	products = models.ManyToManyField(ClientProduct)
	length = models.FloatField(default=.5)
	cloud = models.ManyToManyField(Cloud, blank=True)

	plan = models.CharField(max_length=32, choices=PLAN_CHOICES)

	reference = models.CharField(max_length=128) # Reference code for client to use
	freshbooks_estimate_id = models.CharField(max_length=32, blank=True)
	freshbooks_estimate_num = models.CharField(max_length=32, blank=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	replaced = models.BooleanField(default=False)

	def __str__(self):
		return self.client.get_full_name() + " Cart " + str(self.date_created)

	def get_total_price(self):
		total = 0
		for prd in self.products.all():
			total += product_price(prd, self.plan, self.length)
		for cloud in self.cloud.all():
			total += cloud_price(cloud, self.plan, self.length)
		return total

class Subscription(models.Model):
	client = models.ForeignKey(Client)
	plan = models.CharField(max_length=32, choices=PLAN_CHOICES)
	cart = models.ForeignKey(Cart, blank=True, null=True)
	products = models.ManyToManyField(ClientProduct,blank=True)
	cloud = models.ManyToManyField(Cloud, blank=True)

	length = models.FloatField(default=1)
	subtotal = models.FloatField(default=0.0)
	price = models.FloatField(default=0.0)
	discount_percent = models.FloatField(default=0.0)
	discount_code = models.CharField(max_length=64, blank=True)

	date_begin = models.DateTimeField(blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	freshbooks_invoice_num = models.CharField(max_length=32, blank=True)

	def get_expiration(self):
		return self.date_begin + timedelta(days=self.length*365)

	def __str__(self):
		return self.client.get_full_name() + ": " + self.plan

class PurchaseOrder(models.Model):
	client = models.ForeignKey(Client)
	cart = models.ForeignKey(Cart, blank=True, null=True)
	po_number = models.CharField(max_length=64)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

class EstimateText(models.Model):
	item = models.CharField(max_length=256)
	description = models.TextField()
	cloud = models.ForeignKey(Cloud, null=True, blank=True)

	plan = models.ForeignKey(Plan, null=True, blank=True)
	category = models.ForeignKey(ProductCategory)

	@property
	def short_description(self):
		return truncatechars(self.description, 100)

	def __str__(self):
		return self.item