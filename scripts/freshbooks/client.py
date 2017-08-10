from django.conf import settings

import sys
import requests

try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET



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

def find_client(search_client):
	"""  """
	tree = ET.ElementTree(file='scripts/freshbooks/xml_templates/list_clients.xml')
	root = tree.getroot()
	email = root.find('email')
	email.text = search_client['email']
	input_xml = ET.tostring(root)
	data = input_xml
	headers = {'Content-Type': 'application/xml'}
	r = requests.get(settings.FRESHBOOKS_URL, auth=(settings.FRESHBOOKS_AUTH, ''), headers=headers, data=data)
	# print(r)
	root = ET.fromstring(r.content)
	clients = root[0]
	for client in clients:
		first_name = client.find('{http://www.freshbooks.com/api/}first_name').text
		last_name = client.find('{http://www.freshbooks.com/api/}last_name').text
		email = client.find('{http://www.freshbooks.com/api/}email').text
		client_id = client.find('{http://www.freshbooks.com/api/}client_id').text
		if first_name == search_client['first_name'] and last_name == search_client['last_name'] and email == search_client['email']:
			# response = {
			# 	'client_id': client_id,
			# }
			return client_id

def get_client(client):
	pass

def create_client(client):
	pass