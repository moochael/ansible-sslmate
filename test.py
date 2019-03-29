#!/usr/bin/python

import secrets
import requests
import json
#from ansible.module_utils.basic import AnsibleModule

debug = True

certificate_object_common_name = "davidmacbale.com"
base_api_endpoint = "https://sandbox.sslmate.com/api/v2/{}"

create_api_endpoint = base_api_endpoint.format("certs/{}/".format(certificate_object_common_name))         # https://sandbox.sslmate.com/api/v2/certs/davidmacbale.com/
buy_api_endpoint = base_api_endpoint.format("certs/{}/buy".format(certificate_object_common_name))        # https://sandbox.sslmate.com/api/v2/certs/davidmacbale.com/buy
revoke_api_endpoint = base_api_endpoint.format("certs/{}/revoke".format(certificate_object_common_name))  # https://sslmate.com/api/v2/certs/davidmacbale.com/revoke

def create_certificate_object(domain, debug):
    file_to_open = "openssl/" + domain + ".csr"
    with open('%s' % file_to_open) as csr_file:
        csr_data = csr_file.read()
    cert_data = {'csr': csr_data, 'approval_method': 'dns'}

    request = requests.post(create_api_endpoint, data=cert_data, auth=(secrets.api_key,""))
    pubkey_hash = request.json()['pubkey_hash']

    if debug == 1:
        print("Create Cert Object Response JSON:")
        print(request.json(), end="\n\n")

    return(pubkey_hash)

def buy_certificate(domain, debug):
    request = requests.post(buy_api_endpoint, auth=(secrets.api_key,""))

    if debug == 1:
        print("Buy Cert Response JSON:")
        print(request.json(), end="\n\n")

def revoke_sslmate_certificate(domain, debug):
    cert_data = {'all': 'true'}
    request = requests.post(revoke_api_endpoint, data=cert_data, auth=(secrets.api_key,""))

    if debug == 1:
        print("Revoke Cert Response JSON:")
        print(request.json(), end="\n\n")

def retrive_certificate(domain, hash, debug):
    retrieve_cert_endpoint = base_api_endpoint.format("certs/{}/instances/pubkey_hash:{}".format(certificate_object_common_name, hash))

    request = requests.get(retrieve_cert_endpoint, auth=(secrets.api_key,""))

    if debug == 1:
        print("Retreive Cert Response JSON:")
        print(request.json(), end="\n\n")

try:
    pubkey_hash = (create_certificate_object(certificate_object_common_name, debug=0))

    create_certificate_object(certificate_object_common_name, debug)
    buy_certificate(certificate_object_common_name, debug)
    retrive_certificate(certificate_object_common_name, pubkey_hash, debug)
    #revoke_sslmate_certificate(certificate_object_common_name)

except:
    pass

