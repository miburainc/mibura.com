# Load product information from excel sheet
# Excel sheet provided by Imran
import os,sys

from datetime import datetime, date, timedelta

import django
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

PRODUCT_CATEGORIES = (
	("servers", "Servers"),
	("storage", "Storage Appliances"),
	("network", "Networking"),
	("appliances", "Appliances"),
	("none", "None"),
	("power", "Power")
)

def get_cat(value, prods):
	for i in prods:
		if value==i.category_code:
			return i

	return prods.get(category_code="none")

if BASE_DIR not in sys.path:
	sys.path.append(BASE_DIR)

def App(df):

	product_categories = ProductCategory.objects.all()

	for i,row in df.iterrows():
		model = row['model']
		brand = row['brand']
		category = row['category']

		if(category != "DELETE"):


			category = get_cat(category.lower(), product_categories.all())
			partner_price = row['partner_price']
			retail_price = row['retail_price']


			if partner_price != partner_price:
				partner_price = 0.0
			if retail_price != retail_price:
				retail_price = 0.0	

			if '$' in str(partner_price):
				partner_price = partner_price.replace('$','')

			if '$' in str(retail_price):
				retail_price = retail_price.replace('$','')

			if ',' in str(partner_price):
				partner_price = partner_price.replace(',','')

			if ',' in str(retail_price):
				retail_price = retail_price.replace(',','')

			if type(partner_price) == str:
				partner_price = float(partner_price)

			if type(retail_price) == str:
				retail_price = float(retail_price)

			created = False
			try:
				prod = Product.objects.get(brand=brand, model=model)
				prod.partner_price = partner_price
				prod.retail_price = retail_price
			except ObjectDoesNotExist:
				created = True
				prod = Product(brand=brand, model=model, partner_price=partner_price, retail_price=retail_price, release=date.today() - timedelta(1), category=category, price_silver=1.0, price_gold=1.0, price_black=1.0)

			# Adjust SKU
			cat = ""
			if prod.category == "servers":
				cat = "SRV"
			elif prod.category == "storage":
				cat = "STG"
			elif prod.category == "network":
				cat = "NET"
			elif prod.category == "appliances":
				cat = "APP"

			prod.sku = prod.brand[0].upper() + cat + '-' + '{0:04d}'.format(i)

			prod.save()

			if created:
				print("-- Created --")
			else:
				print("** Loaded")
			print(brand, " ", model, " | ", prod.pk)

# Django setup
if __name__ == '__main__':
	os.chdir(BASE_DIR)
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
	django.setup()
	from support.models import Product, ProductCategory

	df = pd.read_csv("scripts/files/products/MS_EPL_CLEAN.csv", index_col=0, encoding = 'ISO-8859-1')
	App(df)

	df = pd.read_csv("scripts/files/products/SonicWallRawClean.csv", encoding = 'ISO-8859-1', index_col=0)
	App(df)

	df = pd.read_csv("scripts/files/products/0009265995_TS_ALL_070817_CLEAN.csv", index_col=0)
	App(df)

	

	