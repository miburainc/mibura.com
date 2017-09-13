import requests, datetime, json

from django.utils import timezone
from django.conf import settings
from django.db import models



# Create your models here.
class FreshbooksAuth(models.Model):
	code = models.CharField(max_length=150)
	auth = models.CharField(max_length=150)
	refresh = models.CharField(max_length=150)
	expires = models.DateTimeField()

	def get_auth_token(self):
		if self.expires < timezone.now() + datetime.timedelta(hours=1):
			print("expired or expires in under an hour")
			return self.freshbooks_refresh()
		elif self.auth:
			return self.auth
		else:
			return self.freshbooks_auth()
	
	def freshbooks_auth(self):
		url = "https://api.freshbooks.com/auth/oauth/token"
		headers = {'Api-Version': 'alpha', 'Content-Type': 'application/json'}
		payload = {
			'client_secret': settings.FRESHBOOKS_SECRET_KEY,
			'client_id': settings.FRESHBOOKS_CLIENT_ID,
			'grant_type': 'authorization_code', 
			'code': self.code,
			'redirect_uri': 'https://www.mibura.com'
		}
		res = requests.post(url, data=json.dumps(payload), headers=headers)
		print(res)
		print(res.content)
		response_json = res.json()
		if res.status_code == 200:
			# Success
			self.refresh = response_json['refresh_token']
			self.auth = response_json['access_token']
			self.expires = datetime.datetime.now() + datetime.timedelta(0,response_json['expires_in'])
			self.save()
			return response_json['access_token']
		return False


	def freshbooks_refresh(self):
		url = "https://api.freshbooks.com/auth/oauth/token"
		headers = {'Api-Version': 'alpha', 'Content-Type': 'application/json'}
		url = "https://api.freshbooks.com/auth/oauth/token"
		headers = {'Api-Version': 'alpha', 'Content-Type': 'application/json'}
		payload = {
			'client_secret': settings.FRESHBOOKS_SECRET_KEY,
			'client_id': settings.FRESHBOOKS_CLIENT_ID,
			'grant_type': 'refresh_token', 
			'refresh_token': self.refresh,
			'redirect_uri': 'https://www.mibura.com'
		}
		res = requests.post(url, data=json.dumps(payload), headers=headers)
		print(res)
		print(res.content)
		response_json = res.json()
		if res.status_code == 200:
			# Success
			self.refresh = response_json['refresh_token']
			self.auth = response_json['access_token']
			self.expires = datetime.datetime.now() + datetime.timedelta(0,response_json['expires_in'])
			self.save()
			return response_json['access_token']
		return False
