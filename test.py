#!/usr/bin/python

import requests
from ansible.module_utils.basic import AnsibleModule

#sslmate_config_file = "~/.sslmate"
sslmate_config_file = "/Users/david.macbale/.sslmate"

lines = []
with open(sslmate_config_file) as in_file:
    for line in in_file:
        lines.append(line)

for each in lines:
    print(each, end='')

# ops sandbox api key
api_key = ""

domain = "davidmacbale.com"
common_create = "certs/" + domain + "/"
common_buy = "certs/" + domain + "/buy"

base_api_endpoint = "https://sandbox.sslmate.com/api/v2/{}"
create_api_endpoint = base_api_endpoint.format(common_create)
buy_api_endpoint = base_api_endpoint.format(common_buy)

# file_to_open = "openssl/" + domain + ".csr"
# with open('%s' % file_to_open) as csr_file:
#     csr_data = csr_file.read()
# cert_data = {'csr': csr_data, 'approval_method': 'dns'}

# r2 = requests.post(create_api_endpoint, data=cert_data, auth=(api_key,""))
# r3 = requests.post(buy_api_endpoint, auth=(api_key,""))

# request_list = [r2, r3]
# def request_loop(rlist):
#     for r in rlist:
#         print(r.json())
#         print("\n")

# request_loop(request_list)
