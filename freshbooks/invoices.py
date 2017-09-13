from django.conf import settings
from django.utils import timezone
from django.utils.dateformat import DateFormat

import sys, requests, json
from datetime import datetime

from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request

from .models import *
from support.models import *
from support.serializers import ClientSerializer, CartSerializer, CloudSerializer, ProductSerializer


def create_invoice(client, plan, length, items, discount, terms, notes, estimate_id):
	freshbooks_auth = FreshbooksAuth.objects.get(pk=1)

	payload = {
		'invoice': {
			'estimateid': estimate_id,
			'create_date': DateFormat(datetime.now()).format('Y-m-d'),
			'customerid': client['freshbooks_id'],
			'discount_value': str(discount*100),
			'terms': terms,
			'notes': notes,
			'fname': client['first_name'],
			'lname': client['last_name'],
			'organization': client['company'],
			'street': client['street'],
			'street2': client['street2'],
			'city': client['city'],
			'state': client['state'],
			'country': client['country'],
			'code': str(client['zipcode']),
			'lines': items
		}
	}

	url = "https://api.freshbooks.com/accounting/account/VY6wd/invoices/invoices"
	headers = {'Authorization': 'Bearer ' + freshbooks_auth.get_auth_token(), 'Api-Version': 'alpha', 'Content-Type': 'application/json'}

	res = requests.post(url, data=json.dumps(payload), headers=headers)
	# print(res)
	# print(res.content)
	json_response = res.json()

	if res.status_code == 200:
		return json_response['response']['result']['invoice']['invoice_number']
	else:
		return False