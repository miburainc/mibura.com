

# Load product information from excel sheet
# Excel sheet provided by Imran
import os,sys

from datetime import datetime

import django
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist

from openpyxl import load_workbook

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

if BASE_DIR not in sys.path:
	sys.path.append(BASE_DIR)

PRODUCT_CATEGORIES = (
	("servers", "Servers"),
	("storage", "Storage Appliances"),
	("network", "Networking"),
	("appliances", "Appliances"),
)

def get_cat(value):
	for i in PRODUCT_CATEGORIES:
		if value==i[0]:
			return value
	return False

SHEETS = [
	'DELL',
	'HP',
	'ORACLE',
	'CISCO',
	'EMC',
	'HITACHI',
	'NETAPP',
	'IBM',
	'SUPERMICRO',
]

# Main App
def App(wb, name):
	print("*************")
	print("***", name, "***")
	print("*************")

	SHEET_NAME = name
	SHEET_LENGTH = wb[SHEET_NAME].max_row

	for row in range(1,SHEET_LENGTH):
		brand = wb[SHEET_NAME].cell(column=1, row=row).value
		model = wb[SHEET_NAME].cell(column=2, row=row).value
		category = wb[SHEET_NAME].cell(column=3, row=row).value
		print(row, ":", model, ":", category)
		cat_final = get_cat(category.lower())

		brand = brand.replace(" ", "")

		if model != None:
			# print(cat_final)
			# print(row, ": ", model)
			created = False
			try:
				prod = Product.objects.get(brand=brand, model=model, category=cat_final)
			except ObjectDoesNotExist:
				created = True
				prod = Product(brand=brand, model=model, release=datetime.now(), category=cat_final)
				prod.save()

			if prod.price_silver == 0.0:
				prod.price_silver = 1.0
			if prod.price_gold == 0.0:
				prod.price_gold = 1.5
			if prod.price_black == 0.0:
				prod.price_black = 2.0
			if prod.with_cloud == 0.0:
				prod.with_cloud = 1.5
			prod.save()

			if created:
				print("-- Created --")
			else:
				print("** Loaded")
			print(brand, " ", model, " | ", prod.pk)
		else:
			print(row, " is empty")

# Django setup
if __name__ == '__main__':
	os.chdir(BASE_DIR)
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
	django.setup()
	from support.models import Product

	for sheet in SHEETS:
		name = sheet.lower()
		workbook = load_workbook('scripts/files/products/mibura_sss_product_' + name + '.xlsx')
		App(workbook, sheet)