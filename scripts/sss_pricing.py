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
	result = 0.0
	increment = product.product.category.yearly_tax
	
	for i in range(0,diff):
		result = base_price * increment
	print("base:", result)
	for l in range(0,int(length*2)):
		result += base_price + (base_price*increment)
	print("final:",int(length*2), result)
	return result

def unknown_product_price(product, length, yearly_tax, base_price):
	
	age = product.unknown.device_age
	result = base_price * length
	result += base_price * yearly_tax
	print(product.brand, "Price:", result)
	
	return result

def cloud_price(cloud, plan, length, quantity):
	base_price = (plan_prices[plan] * cloud.price_multiplier * quantity) / 2
	result = 0.0
	for l in range(0,int(length*2)):
		result += base_price
	if plan == 'gold' or plan == 'black':
		return 0.0
	return result