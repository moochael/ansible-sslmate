#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: sslmate

short_description: Purchase, renew, revoke, and download a TLS certificate using the SSLMate API.

version_added: "2.7"

description:
    - "This module takes credentials for an existing SSLMate (© 2019 Opsmate, Inc.)
      account and can be used to purchase a new certificate, renew an existing
      certificate, download an existing certificate from the account, or revoke
      an existing certificate all via the SSLMate API."

options:
    common_name:
        description:
            - "The fqdn for the certificate object you would like to manipulate."
        required: true
    sandbox:
        description:
            - "Boolean. Whether or not to use the sandbox SSLMate API."
        required: false
        default: False
    api_key:
        description:
            - "Your credentials (API key) to authenticate to SSLMate. If you're using the sandbox API you'll need a sandbox API key that differs from your production key."
        required: true
    action:
        description:
            - "Description here"
        required: true
    csr:
        description:
            - "The path to the csr file."
        required: false
    publickey_hashed:
        description:
            - "The hash of the public key used to identify the certificate object on SSLMate."
        required: false

author:
    - David Macbale (@moochael)
'''

EXAMPLES = '''

'''

RETURN = '''

'''

from ansible.module_utils.basic import AnsibleModule
import requests
import json

debug = True
use_sandbox = True

if use_sandbox == True:
    base_api_endpoint = "https://sandbox.sslmate.com/api/v2/{}"
else:
    base_api_endpoint = "https://sslmate.com/api/v2/{}"

def create_certificate_object(domain, csr, api_key, debug=0):
    file_to_open = csr
    with open('%s' % file_to_open) as csr_file:
        csr_data = csr_file.read()
    cert_data = {'csr': csr_data, 'approval_method': 'dns'}

    create_api_endpoint = base_api_endpoint.format("certs/{}/".format(domain))
    request = requests.post(create_api_endpoint, data=cert_data, auth=(api_key,""))
    publickey_hashed = request.json()['pubkey_hash']

    if debug == 1:
        print("Create Cert Object Response JSON:")
        print(request.json())

    return(publickey_hashed)

def buy_certificate(domain, api_key, debug=0):
    buy_api_endpoint = base_api_endpoint.format("certs/{}/buy".format(domain))
    request = requests.post(buy_api_endpoint, auth=(api_key,""))

    if debug == 1:
        print("Buy Cert Response JSON:")
        print(request.json())

def retrieve_certificate_object(domain, hash, api_key, debug=0):
    retrieve_cert_endpoint = base_api_endpoint.format("certs/{}/instances/pubkey_hash:{}".format(domain, hash))

    request = requests.get(retrieve_cert_endpoint, auth=(api_key,""))

    if debug == 1:
        print("Retreive Cert Response JSON:")
        print(request.json())

def revoke_sslmate_certificate(domain, csr, api_key, debug=0):
    revoke_api_endpoint = base_api_endpoint.format("certs/{}/revoke".format(domain))
    cert_data = {'all': 'true'}
    request = requests.post(revoke_api_endpoint, data=cert_data, auth=(api_key,""))

    if debug == 1:
        print("Revoke Cert Response JSON:")
        print(request.json())

    publickey_hashed = (create_certificate_object(domain, csr, api_key, debug=0))
    retrieve_certificate_object(domain, publickey_hashed, api_key, debug)


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        action=dict(type='str', required=True, choices=['buy', 'renew', 'revoke']),
        api_key=dict(type='str', required=True),
        common_name=dict(type='str', required=True),
        csr=dict(type='str', required=False),
        publickey_hashed=dict(type='str', required=False),
        sandbox=dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    if module.params.get('action') == 'buy':
        api_key = module.params.get('api_key')
        common_name = module.params.get('common_name')
        csr = module.params.get('csr')

        create_certificate_object(common_name, csr, api_key, debug=0)
        buy_certificate(common_name, api_key, debug=0)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
