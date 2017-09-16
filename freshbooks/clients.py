import sys, requests

from django.conf import settings

from .models import *


try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET


def create_client(client_obj):
	freshbooks_auth = FreshbooksAuth.objects.get(pk=1)
	# print(client_obj)
	url = "https://api.freshbooks.com/accounting/account/VY6wd/users/clients"
	headers = {'Authorization': 'Bearer ' + freshbooks_auth.get_auth_token(), 'Api-Version': 'alpha', 'Content-Type': 'application/json'}
	payload = {
		'client': { 
			'email': client_obj['email'],
			'fname': client_obj['first_name'],
			'lname': client_obj['last_name'],
			'organization': client_obj['company'],
			'home_phone': client_obj['phone']
		}
	}
	res = requests.post(url, data=json.dumps(payload), headers=headers)
	json_response = res.json()

	if res.status_code == 200 or res.status_code == 201:
		return json_response['response']['result']['client']['id']
	else:
		return False

def list_clients(page):
	freshbooks_auth = FreshbooksAuth.objects.get(pk=1)
	url = "https://api.freshbooks.com/accounting/account/VY6wd/users/clients?page=" + str(page)
	headers = {'Authorization': 'Bearer ' + freshbooks_auth.get_auth_token(), 'Api-Version': 'alpha', 'Content-Type': 'application/json'}
	res = requests.get(url, data=None, headers=headers)
	json_response = res.json()

	clients = json_response['response']['result']
	
	return clients

def find_client(client_fname, client_lname, client_email):
	"""  """
	results = list_clients(1)

	for client in results['clients']:
		first_name = client['fname']
		last_name = client['fname']
		email = client['fname']
		client_id = client['id']
		if first_name == client_fname and last_name == client_lname:
			return client_id

	if results['pages'] > 1:
		for i in range(2, results['pages']):
			results = list_clients(i)
			for client in results['clients']:
				first_name = client['fname']
				last_name = client['fname']
				email = client['fname']
				client_id = client['id']
				if first_name == client_fname and last_name == client_lname:
					return client_id
	return False

def get_client(client):
	pass