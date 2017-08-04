from django.db import models

PLAN_CHOICES = (
	("slvr", "Silver"),
	("gold", "Gold"),
	("blck", "Black"),
)

PRODUCT_CATEGORIES = (
	("servers", "Servers"),
	("storage", "Storage Appliances"),
	("firewall", "Firewalls"),
	("netswitch", "Network Switches"),
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


class Subscription(models.Model):
	client = models.ForeignKey(Client)
	plan = models.CharField(max_length=32, choices=PLAN_CHOICES)

	price = models.FloatField(default=0.0)
	discount_code = models.CharField(max_length=64, blank=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)


class Cart(models.Model):
	email = models.CharField(max_length=128)
	client = models.ForeignKey(Client)
	products = models.ManyToManyField(Product)

	reference = models.CharField(max_length=128) # Reference code for client to use

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.client.name + " Cart " + self.date_created


class ClientProduct(models.Model):
	client = models.ForeignKey(Client)
	product = models.ForeignKey(Product)

	serial_number = models.CharField(max_length=128, blank=True)
	device_age = models.IntegerField(default=0)
	additional_info = models.TextField(blank=True)
	cloud = models.ForeignKey(Cloud, null=True)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

