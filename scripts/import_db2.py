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

def App(csv):








# Django setup
if __name__ == '__main__':
	os.chdir(BASE_DIR)
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
	django.setup()
	from support.models import Product, ProductCategory

	csv = pd.read_csv("0009265995_TS_ALL_070817_CLEAN.csv", index_col=0)
	App(csv)

	csv = pd.read_csv("SonicWallRawClean.csv", encoding = 'ISO-8859-1', index_col=0)
