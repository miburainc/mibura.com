import requests  
import json
import os

"""
    Initial OAuth 
    Set these values to retrieve the oauth token
"""

# TODO: Export these into the OS or have a secure method of storing this data
crmorg = 'https://mibura.crm.dynamics.com'  
clientid = '3b27a862-47bb-4f3b-a7a6-ede77d81e67e' 
username = 'bendres@mibura.com'  
userpassword = 'Gd&]VR/B*2%$U'  
tokenendpoint = 'https://login.microsoftonline.com/9071f836-52ac-48c6-aaa3-bc4dea97e4d0/oauth2/token' 
authorizationendpoint = 'https://login.windows.net/9071f836-52ac-48c6-aaa3-bc4dea97e4d0/oauth2/authorize'
tenant_id = '9071f836-52ac-48c6-aaa3-bc4dea97e4d0'
client_secret = '65sAbmi9vXaU6QfCNXcXfOaUR4xb7PF7MEqvEVkOcQs='
# End TODO

crmwebapi = 'https://mibura.api.crm.dynamics.com/api/data/v8.2' 
 
tokenpost = {  
    'client_id':clientid,
    'client_secret':client_secret,
    'resource':crmorg,
    'oauthUrl':authorizationendpoint,
    'username':username,
    'password':userpassword,
    'grant_type':'password'
}

tokenres = requests.post(tokenendpoint, data=tokenpost)

accesstoken = ''
 
try:  
    accesstoken = tokenres.json()['access_token']
except(KeyError):  
    print('Could not get access token')


"""
##################################################################
                            CREATE
##################################################################
"""

def createAccount():
    """
    POST [Organization URI]/api/data/v8.2/accounts HTTP/1.1
    Content-Type: application/json; charset=utf-8
    OData-MaxVersion: 4.0
    OData-Version: 4.0
    Accept: application/json
    """

    if(accesstoken!=''):    
        crmrequestheaders = {
            'Authorization': 'Bearer ' + accesstoken,
            'Content-Type': 'application/json; charset=utf-8',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json'
        }
     
        #make the crm request
        contactObj={
            "name": "Test Quote Name",
            "description": "This is the description of the sample account",
        };

        crmres = requests.post(crmwebapi+'/accounts', headers=crmrequestheaders, data=json.dumps(contactObj))
        print(crmres.value())

def createQuote():
    """
    POST [Organization URI]/api/data/v8.2/accounts HTTP/1.1
    Content-Type: application/json; charset=utf-8
    OData-MaxVersion: 4.0
    OData-Version: 4.0
    Accept: application/json
    """

    if(accesstoken!=''):    
        crmrequestheaders = {
            'Authorization': 'Bearer ' + accesstoken,
            'Content-Type': 'application/json; charset=utf-8',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json'
        }
     
        #make the crm request
        contactObj={
            "name": "Test Quote Name",
            "description": "This is the description of the sample account",
        };

        crmres = requests.post(crmwebapi+'/quotes', headers=crmrequestheaders, data=json.dumps(contactObj))


"""
##################################################################
                            READ
##################################################################
"""    

def accessAccounts(): 
    if(accesstoken!=''):  
        crmrequestheaders = {
            'Authorization': 'Bearer ' + accesstoken,
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8',
            'Prefer': 'odata.maxpagesize=500',
            'Prefer': 'odata.include-annotations=OData.Community.Display.V1.FormattedValue'
        }
     
        crmres = requests.get(crmwebapi+'/accounts?$select=name', headers=crmrequestheaders)
     
        try:
            crmresults = crmres.json()
     
            for x in crmresults['value']:
                print (x['name'])
        except KeyError:
            print('Could not parse CRM results')

def accessQuotes(): 
    if(accesstoken!=''):  
        crmrequestheaders = {
            'Authorization': 'Bearer ' + accesstoken,
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=utf-8',
            'Prefer': 'odata.maxpagesize=500',
            'Prefer': 'odata.include-annotations=OData.Community.Display.V1.FormattedValue'
        }
     
        crmres = requests.get(crmwebapi+'/quotes?$select=name', headers=crmrequestheaders)
     
        try:
            crmresults = crmres.json()
     
            for x in crmresults['value']:
                print (x['name'])
        except KeyError:
            print('Could not parse CRM results')

"""
##################################################################
                            UPDATE
##################################################################
"""    

def updateContact(accesstoken, contactid):
    """
    PATCH [Organization URI]/api/data/v8.2/accounts(00000000-0000-0000-0000-000000000001) HTTP/1.1
    Content-Type: application/json
    OData-MaxVersion: 4.0
    OData-Version: 4.0
    """
    if(accesstoken!=''):    
        crmrequestheaders = {
            'Authorization': 'Bearer ' + accesstoken,
            'Content-Type': 'application/json',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0'
        }
        
        """
            Add more parameters within the contactObj to initialize more fields
        """
           
        contactObj={
            "name": "Sample Account",
            "creditonhold": false,
            "address1_latitude": 47.639583,
            "description": "This is the description of the sample account",
            "revenue": 5000000,
            "accountcategorycode": 1   
        };
        crmres = requests.put(crmwebapi+'/contacts('+contactid+')/firstname', headers=crmrequestheaders, data=json.dumps(contactObj))
        print(crmres)

"""
##################################################################
                            DELETE
##################################################################
"""    

def deleteContact():
    """
    DELETE [Organization URI]/api/data/v8.2/accounts(00000000-0000-0000-0000-000000000001)/description HTTP/1.1
    Content-Type: application/json
    OData-MaxVersion: 4.0
    OData-Version: 4.0
    """
    if(accesstoken!=''):  
        crmrequestheaders = {
            'Authorization': 'Bearer ' + accesstoken,
            'Content-Type': 'application/json',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0'
        }

        crmres = requests.delete(crmwebapi+'/accounts('+ accountid +')', headers=crmrequestheaders)
        print(crmres)
 



