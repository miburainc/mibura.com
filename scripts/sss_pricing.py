from datetime import datetime, date
import math

from support.models import *

def months_between(date1,date2):
	if date1>date2:
		date1,date2=date2,date1
	m1=date1.year*12+date1.month
	m2=date2.year*12+date2.month
	months=m2-m1
	if date1.day>date2.day:
		months-=1
	elif date1.day==date2.day:
		seconds1=date1.hour*3600+date1.minute+date1.second
		seconds2=date2.hour*3600+date2.minute+date2.second
		if seconds1>seconds2:
			months-=1
	return months

plan_prices = {
	'silver': 49,
	'gold': 99,
	'black': 499
}

def product_price(product, plan, length):
	print("product_price")
	print(product.product)
	print(plan)
	prd_plan_name = 'price_'+plan
	product_plan_multiplier = getattr(product.product, prd_plan_name)
	base_price = (plan_prices[plan] * product.product.category.price_multiplier * product_plan_multiplier) / 2
	date_start = product.product.release

	date_now = date.today()
	diff = math.floor(months_between(date_start, date_now) / 6)

	increment = product.product.category.yearly_tax

	result = base_price * increment * diff
	result += base_price * length * 2

	return result

def unknown_product_price(product, length, yearly_tax, base_price):
	
	age = product.unknown.device_age

	print(age)
	print(length)
	print(base_price)
	print(yearly_tax)

	result = base_price * length
	result += base_price * age * yearly_tax

	return result

def cloud_price(cloud, plan, length, quantity):

	base_price = (plan_prices[plan] * (cloud.price_multiplier + cloud.quantity_multiplier * quantity)) / 2
	
	result = base_price * length * 2

	if plan == 'gold' or plan == 'black':
		return 0.0

	return result