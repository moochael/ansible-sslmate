#!/usr/local/bin/python3

# openssl req -new -sha256 -key example.com.key -out example.com.csr

import requests

api_key = ""
common_create = "certs/example.com/"
common_buy = "certs/example.com/buy"

base_api_endpoint = "https://sandbox.sslmate.com/api/v2/{}"
create_api_endpoint = base_api_endpoint.format(common_create)
buy_api_endpoint = base_api_endpoint.format(common_buy)

with open("/Users/davidmacbale/repos/ansible-sslmate/example.com.csr") as csr_file:
    csr_data = csr_file.read()
cert_data = {'csr': csr_data, 'approval_method': 'email', 'approver_email': 'example@example.com' }

# r1 = requests.get(api_endpoint, auth=(api_key,""))
# print(r1.json())

# r2
# curl https://sslmate.com/api/v2/certs/example.com \
#    -u 123_sampleapikey: \
#    --data-urlencode csr=$'-----BEGIN CERTIFICATE REQUEST-----...' \
#    -d approval_method=email \
#    -d approver_email=webmaster@example.com \

r2 = requests.post(create_api_endpoint, data=cert_data, auth=(api_key,""))

r3 = requests.post(buy_api_endpoint, auth=(api_key,""))

request_list = [r2, r3]
def request_loop(rlist):
    for r in rlist:
        print(r.json())

request_loop(request_list)
