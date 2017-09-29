import stripe
from datetime import datetime

from django.conf import settings
from django.db import models

from support.models import Client, Cart, Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY

payment_type_choices = (
	('creditcard', 'Credit Card'),
	('achplaid', 'Bank ACH - Plaid'),
	('achstripe', 'Bank ACH - Stripe'),
	('paypal', 'Paypal'),
	('po', 'Purchase Order')
)

class StripeClient(models.Model):
	client = models.OneToOneField(Client)
	customer_id = models.CharField(max_length=128)
	bank_id = models.CharField(max_length=128, blank=True)
	bank_type = models.CharField(max_length=32, blank=True)
	bank_verified = models.BooleanField(default=False)

	@classmethod
	def create(cls, client):
		# Make API calls to Stripe
		# stripe_customer_id = stripe.create_customer(asdlfkajsd)
		try:
			customer = stripe.Customer.create(
				description=client.get_full_name() + " customer",
				email=client.email,
				metadata={"created": datetime.now(), "first_name": client.first_name, "last_name": client.last_name, "company": client.company}
			)
		except stripe.error.InvalidRequestError as e:
			return e

		stripe_customer_id = customer['id']

		stripe_client = cls(client=client, customer_id=stripe_customer_id)
		return stripe_client

	def stripe_create_bank(self, token):
		customer = stripe.Customer.retrieve(self.customer_id)
		request = customer.sources.create(source=token)
		self.bank_id = request['id']
		self.save()
		return request

	def stripe_verify_bank_ach(self, amt1, amt2):
		# Verify bank account
		# Allows ACH payments with stripe
		# uses two micro-deposits into bank
		customer = stripe.Customer.retrieve(self.customer_id)
		bank_account = customer.sources.retrieve(self.bank_id)

		try:
			request = bank_account.verify(amounts=[amt1, amt2])
		except stripe.error.InvalidRequestError as e:
			body = e.json_body
			err  = body.get('error', {})
			return {
				'status': 400,
				'error': err.get('message')
			}

		if request['status'] == 'verified':
			self.bank_verified = True
			self.bank_type = request['account_holder_type']
			self.save()

		return request

	def __str__(self):
		return self.client.get_full_name() + " Stripe Client Obj"

class PaymentManager(models.Manager):
	def create_stripe_creditcard(self, client, payment_token, amount):
		payment = self.create(token=payment_token, amount=amount)
		payment.payment_type="creditcard"
		return payment

	def create_stripe_ach(self, payment_token):
		payment = self.create(title=title)
		# do something with the book
		payment.payment_type="achstripe"
		return payment

	def create_plaid(self, client, payment_token, amount):
		payment = self.create(token=payment_token, amount=amount)
		# do something with the book
		payment.payment_type="achplaid"
		return payment

	def create_paypal(self, client, payment_token, amount):
		payment = self.create(token=payment_token, amount=amount)
		# do something with the book
		payment.payment_type="paypal"
		return payment

	def create_purchaseorder(self, client, po_number):
		payment = self.create(token=po_number)
		payment.payment_type="po"
		return payment

class Payment(models.Model):
	# customer = models.ForeignKey(Customer) # After adding customer login accounts
	client = models.ForeignKey(Client)
	cart = models.ForeignKey(Cart, blank=True, null=True)
	
	payment_type = models.CharField(max_length=64, choices=payment_type_choices)
	token = models.CharField(max_length=128)
	secondary_token = models.CharField(max_length=128, blank=True) # Payment auth token or completion token, optional
	amount = models.FloatField(default=0.0)

	completed = models.BooleanField(default=False)

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)

	objects = PaymentManager()

	def process(self):
		# Complete payment

		# If ACH Stripe
		if self.payment_type == "achstripe":
			token = self.client.stripeclient.bank_id
			# stripe.create_payment(token=token, amount=self.amount)


		return True
	

class Receipt(models.Model):
	# customer = models.ForeignKey(Customer) # After adding customer login accounts
	subscription = models.ForeignKey(Subscription)
	payment_type = models.CharField(max_length=64, choices=payment_type_choices)
	amount = models.FloatField(default=0.0)
	discount_percentage = models.FloatField(default=0.0)
	# coupons = models.ManyToManyField(Coupon) # After adding coupons to system
	# discounts = models.ManyToManyField(Discount) # After adding discounts/sales to system

	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)