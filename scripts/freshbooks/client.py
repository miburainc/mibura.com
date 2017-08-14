from django.conf import settings

import sys
import requests

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

def create_client(client_obj):
	print(client_obj)
	tree = ET.ElementTree(file='scripts/freshbooks/xml_templates/create_client.xml')
	root = tree.getroot()
	client = root[0]

	first_name = client.find('first_name')
	first_name.text = client_obj['first_name']

	last_name = client.find('last_name')
	last_name.text = client_obj['last_name']

	email = client.find('email')
	email.text = client_obj['email']

	organization = client.find('organization')
	organization.text = client_obj['company']

	phone = client.find('work_phone')
	phone.text = client_obj['phone']

	street1 = client.find('p_street1')
	street1.text = client_obj['street']

	street2 = client.find('p_street2')
	if client_obj['street2'] != '':
		street2.text = client_obj['street2']
	else:
		client.remove(street2)

	city = client.find('p_city')
	city.text = client_obj['city']

	state = client.find('p_state')
	state.text = client_obj['state']

	country = client.find('p_country')
	country.text = client_obj['country']

	zipcode = client.find('p_code')
	zipcode.text = client_obj['zipcode']

	data = ET.tostring(root)

	headers = {'Content-Type': 'application/xml'}
	r = requests.post(settings.FRESHBOOKS_URL, auth=(settings.FRESHBOOKS_AUTH, ''), headers=headers, data=data)
	root = ET.fromstring(r.content)
	client_id = root[0]
	return client_id.text

def list_clients(client):
	tree = ET.ElementTree(file='scripts/freshbooks/xml_templates/list_clients.xml')
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
	tree = ET.ElementTree(file='scripts/freshbooks/xml_templates/list_clients.xml')
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