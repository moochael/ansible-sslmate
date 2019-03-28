#!/usr/bin/python

import secrets
import requests
import json
#from ansible.module_utils.basic import AnsibleModule

sslmate_config_file = "/Users/david.macbale/.sslmate"
certificate_object_common_name = "davidmacbale.com"
base_api_endpoint = "https://sandbox.sslmate.com/api/v2/{}"

common_create_uri = "certs/" + certificate_object_common_name + "/" # https://sandbox.sslmate.com/api/v2/certs/davidmacbale.com/
common_buy_uri = "certs/" + certificate_object_common_name + "/buy" # https://sandbox.sslmate.com/api/v2/certs/davidmacbale.com/buy
revoke_uri = "certs/" + certificate_object_common_name + "/revoke" # https://sslmate.com/api/v2/certs/COMMON_NAME/revoke

create_api_endpoint = base_api_endpoint.format(common_create_uri)
buy_api_endpoint = base_api_endpoint.format(common_buy_uri)
revoke_api_endpoint = base_api_endpoint.format(revoke_uri)


# test format method
apiurl = "https://sandbox.sslmate.com/api/v2/{}"
apiuri = "certs/{}/buy/"

buyapiurl = apiurl.format(apiuri.format(certificate_object_common_name))
print(buyapiurl)
# https://sandbox.sslmate.com/api/v2/certs/davidmacbale.com/buy/


def create_certificate_object(domain):
    file_to_open = "openssl/" + certificate_object_common_name + ".csr"
    with open('%s' % file_to_open) as csr_file:
        csr_data = csr_file.read()
    cert_data = {'csr': csr_data, 'approval_method': 'dns'}

    request = requests.post(create_api_endpoint, data=cert_data, auth=(secrets.api_key,""))
    print(request.json())

def buy_certificate(domain):
    request = requests.post(buy_api_endpoint, auth=(secrets.api_key,""))
    print(request.json())

def revoke_sslmate_certificate(domain):
    cert_data = {'all': 'true'}
    request = requests.post(revoke_api_endpoint, data=cert_data, auth=(secrets.api_key,""))
    print(request.json())

def retrive_certificate(domain):

    request1 = requests.get(retrieve_cert_endpoint, auth=(secrets.api_key,""))

    retreive_cert_uri = "certs/" + certificate_object_common_name + "/instances/pubkey_hash:" + json_data['pubkey_hash'] # https://sandbox.sslmate.com/api/v2/certs/davidmacbale.com/instances/pubkey_hash:[HASH]
    retrieve_cert_endpoint = base_api_endpoint.format(retreive_cert_uri)
    request2 = requests.get(retrieve_cert_endpoint, auth=(secrets.api_key,""))
    json_data = json.loads(request.text)
    #print(json_data['pubkey_hash'])

    print(request.json())

try:
    #create_certificate_object(certificate_object_common_name)
    #buy_certificate(certificate_object_common_name)
    #retrive_certificate(certificate_object_common_name)
    #revoke_sslmate_certificate(certificate_object_common_name)
    pass

except:
    pass

