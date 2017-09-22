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

if BASE_DIR not in sys.path:
	sys.path.append(BASE_DIR)

def App(df):

	for i,row in df.iterrows():
		category = row['category']
		sub_category = row['subcategory']
		name = row['name']

		created = False

		try:
			cloud = Cloud.objects.get(name=name)
		except ObjectDoesNotExist:
			print("Error, cloud name is not in database:",name)
			print("Exiting...")
			return(0)

		try:
			addon = CloudAddOn.objects.get(category=category, sub_category=sub_category, cloud=cloud)
		except ObjectDoesNotExist:
			created = True
			addon = CloudAddOn(category=category, sub_category=sub_category, cloud=cloud)

		addon.save()
		
		if created:
			print("-- Created --")
		else:
			print("** Loaded")
		print(category, " ", sub_category, " | ", cloud.name)

# Django setup
if __name__ == '__main__':
	os.chdir(BASE_DIR)
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
	django.setup()
	from support.models import Cloud, CloudAddOn

	df = pd.read_csv("scripts/files/products/azure_addons.csv")
	App(df)