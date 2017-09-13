from django.conf import settings

import sys, requests

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET


def create_client(client_obj):
	# print(client_obj)
	url = "https://api.freshbooks.com/accounting/account/VY6wd/users/clients"
	headers = {'Authorization': 'Bearer <Bearer Token>', 'Api-Version': 'alpha', 'Content-Type': 'application/json'}
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

	if res.status_code == 200 or res.status_code == 201:
		return json_response['response']['result']['client']['id']
	else:
		return False


def list_clients(client):
	root = tree.getroot()
	email = root.find('email')
	email.text = client['email']
	input_xml = ET.tostring(root)
	data = input_xml
	print('\n\n')
	headers = {'Content-Type': 'application/xml'}
	r = requests.get(settings.FRESHBOOKS_URL, auth=(settings.FRESHBOOKS_AUTH, ''), headers=headers, data=data)
	# print(r)
	print(r.content)
	print('\n')
	root = ET.fromstring(r.content)
	print(root)
	clients = root[0]
	print(clients)
	for c in clients:
		print('client_id', c.find('{http://www.freshbooks.com/api/}client_id').text)

def find_client(client_fname, client_lname, client_email):
	"""  """
	tree = ET.ElementTree(file='freshbooks/xml_templates/list_clients.xml')
	root = tree.getroot()

	email = root.find('email')
	email.text = client_email
	input_xml = ET.tostring(root)
	data = input_xml
	headers = {'Content-Type': 'application/xml'}
	r = requests.get(settings.FRESHBOOKS_URL, auth=(settings.FRESHBOOKS_AUTH, ''), headers=headers, data=data)
	root = ET.fromstring(r.content)

	client_id = ""

	clients = root[0]
	for client in clients:
		first_name = client.find('{http://www.freshbooks.com/api/}first_name').text
		last_name = client.find('{http://www.freshbooks.com/api/}last_name').text
		email = client.find('{http://www.freshbooks.com/api/}email').text
		client_id = client.find('{http://www.freshbooks.com/api/}client_id').text
		if first_name == client_fname and last_name == client_lname:
			return client_id

	return False

def get_client(client):
	pass