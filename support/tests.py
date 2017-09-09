from django.test import TestCase, Client
import json

# Create your tests here.
# Test #1: get-or-create-client API endpoint
class SupportTestCase(TestCase):
    def test_get_create_client(self):
        c = Client()
        data_raw = {
            "first_name": "Testing Firstname",
            "last_name": "Testing Lastname",
            "company": "Testing Company",
            "phone": "3101234567",
            "email": "testing@domain.com",
            "street": "123 Testing Blvd",
            "city": "Los Angeles",
            "state": "CA",
            "country": "USA",
            "zipcode": "90000"
            # "street2": ""
            # "pk": 6
        }
        data_str = json.dumps(data_raw)
        
        response = c.post('/support/get-or-create-client/', content_type='application/json', data=data_str)
        self.assertEqual(response.status_code, 201)
