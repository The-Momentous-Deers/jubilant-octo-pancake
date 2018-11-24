import json, time, pprint
from urllib.request import Request, urlopen

base_url = 'https://play.railsbank.com/'

# The next line contains get post and put helper functions, which should be replaced with a library of your choice in production code
custom_fetch = lambda method, relative_url, body=None: json.loads(urlopen(Request(base_url+relative_url, data=json.dumps(body).encode('utf8'), method=method, headers={'Content-Type': 'application/json', 'Authorization': 'API-Key ' + api_key, 'Accept': 'application/json'})).read().decode('utf-8')); post = lambda url, body=None: custom_fetch("POST", url, body); get = lambda url: custom_fetch("GET", url); put = lambda url, body=None: custom_fetch("PUT", url, body)

# Make sure to replace `***EXAMPLE KEY***` in the next line with your api key of form <key_id>#<key_secret>
api_key = 'iyg7oiwx5c6t462y80vytq0qtotredni#u9cgcudk4b95czmprv809jmb2ltkd971j0d3npvgq9vxfelrfylcg3x3hn0a8siy'


class RailsbankRequest:

    ledger_id = "5bf951a0-8c73-437c-ae59-ac60a0f9847e"

    def __init__(self):
        response = get('v1/customer/me')
        pprint.pprint(response)
        self.customer_id = response['customer_id']

    def getEnduser(self):
        response = post(
            'v1/customer/endusers', {
                'person': {
                    'name': 'Jane',
                    'email': 'jane@email.com',
                    'address': {
                        'address_iso_country': 'GB'
                    }
                }
            })
        pprint.pprint(response)
        self.enduser_id = response['enduser_id']

        '''
        Enduser is not ready immediately because of ongoing validity checks.
        '''
        response = get('v1/customer/endusers/' + str(self.enduser_id) + '/wait')
        pprint.pprint(response)

    def makeLedger(self):
        '''
        Creating ledger assigned to our enduser and assigning iban to it.
        '''
        bank_example_product = 'ExampleBank-EUR-1'
        response = post(
            'v1/customer/ledgers', {
                'holder_id': self.customer_id, # this was self.enduser_id
                'partner_product': bank_example_product,
                'asset_class': 'currency',
                'asset_type': 'eur',
                'ledger-type': 'ledger-type-single-user',
                'ledger-who-owns-assets': 'ledger-assets-owned-by-me',
                'ledger-primary-use-types': ['ledger-primary-use-types-payments'],
                'ledger-t-and-cs-country-of-jurisdiction': 'GB'
            })
        pprint.pprint(response)
        self.ledger_id = response['ledger_id']
        print(self.ledger_id)
        pprint.pprint(response)

    def getBalance(self):
        response = get('v1/customer/ledgers/' + str(self.ledger_id))
        return response['amount']
