from django.test import TestCase, Client
from .models import ProductCategory
import json

# Create your tests here.
# Test #1: get-or-create-client API endpoint
class SupportTestCase(TestCase):

    sample_client_data_raw = {
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
    sample_client_data = json.dumps(sample_client_data_raw)

    sample_product_data_default = {
        "brand": "Dell",
        "model": "PowerEdgeT30",
        "sku": "D-0301",
        "category": {
            "name": "Servers",
            "category_code": "servers",
            "yearly_tax": 0.1,
            "price_multiplier": 1},
            "price_silver": 1,
        "price_gold": 1,
        "price_black": 1,
        "release": "2017-08-08",
        "sn": "1234567890",
        "age":"12",
        "info":"1"}

    sample_product_data_customized = {
        "brand": "Testing non-existent brand",
        "model": "New testing model",
        "sku": "T-E-S-T01",
        "category": {
            "name": "UFO",
            "category_code": "ufo",
            "yearly_tax": 0.9,
            "price_multiplier": 1},
        "price_silver": 1.5,
        "price_gold": 2,
        "price_black": 2.5,
        "release": "2017-08-08",
        "sn": "1234567890",
        "age":"1",
        "info":"Hello world"}

    
    def setUp(self):
        ProductCategory.objects.create(name="Servers", category_code="servers")
        ProductCategory.objects.create(name="None", category_code="none")

    def test_get_create_client(self):
        c = Client()
        response = c.post('/support/get-or-create-client/', content_type='application/json', data=self.sample_client_data)
        self.assertEqual(response.status_code, 201)
        # Post the same content again
        response = c.post('/support/get-or-create-client/', content_type='application/json', data=self.sample_client_data)
        self.assertEqual(response.status_code, 200)

    # create cart of a pre-defined Product
    def test_get_create_cart_default(self):
        c = Client()
        # get or create a client first and get the client's PK (identifier)
        create_client_response = c.post('/support/get-or-create-client/', content_type='application/json', data=self.sample_client_data)
        self.assertEqual(create_client_response.status_code, 201)
        client_pk = create_client_response.content.decode("utf-8") 

        # create a cart based on this client
        cart_data = json.dumps({
            "email": self.sample_client_data_raw['email'],
            "client": int(client_pk),
            "reference": "wz8mDCrJ",  # a random reference number
            "products": [self.sample_product_data_default],
            "plan": "silver",
            "length": 1})
        create_cart_response = c.post('/support/get-or-create-cart/', content_type='application/json', data=cart_data)
        self.assertEqual(create_cart_response.status_code, 200)

    # create cart of two products, one default Product and one customized Product
    def test_get_create_cart_customized(self):
        c = Client()
        # get or create a client first and get the client's PK (identifier)
        create_client_response = c.post('/support/get-or-create-client/', content_type='application/json', data=self.sample_client_data)
        self.assertEqual(create_client_response.status_code, 201)
        client_pk = create_client_response.content.decode("utf-8") 

        # create a cart based on this client        
        cart_data = json.dumps({
            "email": self.sample_client_data_raw['email'],
            "client": int(client_pk),
            "reference": "wz8mDCrJ",  # a random reference number
            "products": [self.sample_product_data_default, self.sample_product_data_customized],
            "plan": "silver",
            "length": 1})
        create_cart_response = c.post('/support/get-or-create-cart/', content_type='application/json', data=cart_data)
        self.assertEqual(create_cart_response.status_code, 200)

    # def test_get_estimate_pdf(self):
