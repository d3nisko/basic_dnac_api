#!/usr/bin/env python

import requests
from requests.auth import HTTPBasicAuth
from dnac_config import DNAC_IP, DNAC_PORT, USERNAME, PASSWORD
from pprint import pprint

def get_auth_token(dnac_ip, dnac_port, username, password):
    base_url = 'https://{}:{}'.format(dnac_ip, dnac_port)
    token_endpoint = '/dna/system/api/v1/auth/token'
    #alternative endpoint for the auth token is api/system/v1/auth/token
    url = base_url + token_endpoint

    auth = HTTPBasicAuth(username, password)

    response = requests.request('POST', url, auth=auth, verify=False)
    
    if response.status_code == 200:
        token = response.json()['Token']
        return token
    else:
        print('Something went wrong. Not able to get the authorization token')
        print('Status code is: {}'.format(response.status_code))
        print(response.text)
        exit()


def get_device_list(dnac_ip, dnac_port, token):
    #The function gets device list from the DNAC api and return dict
    #with all data. It is yet raw data and function doesn't care about
    #formatting.

    base_url = 'https://{}:{}'.format(dnac_ip, dnac_port)
    endpoint = '/dna/intent/api/v1/network-device'

    url = base_url + endpoint

    headers = { 'x-auth-token': token, 'Content-Type': 'application/json' }

    #optionally we can apply filter to the retrieved data
    #querystr = {"macAddress":"00:c8:8b:80:bb:00","managementIpAddress":"10.10.22.74"}
    #The query string is passeed to request using params keyword
    #request('GET', url, headers=headers, params=querystr, verify=False)

    response = requests.request('GET', url, headers=headers, verify=False)
    
    if response.status_code == 200:
        return response.json()
    else:
        print('Something went wrong. Not able to retrieve the list of \
        devices.')
        print(response.text)
        exit()

def get_all_interfaces(dnac_ip, dnac_port, token, device_id=None):
    #The function returns all interfaces. The function optinoally gets 
    #parameters for query and alters the api call if we provide a filter.
    #The filter should specify device for which we would like to get interfaces

    base_url = 'https://{}:{}'.format(dnac_ip, dnac_port)
    headers = {
        'x-auth-token': token,
        'Content-Type': 'application/json'
        }
    
    
    if device_id:
        endpoint = '/dna/intent/api/v1/interface/network-device/' + device_id
    else:
        endpoint = '/dna/intent/api/v1/interface'

    url = base_url + endpoint

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        return response.json()
    else:
        print("Something went wrong. Not able to retrieve the list of\
        interfaces")
        print("The status code is: {}".format(response.status_code))
        print(response.text)




if __name__ == "__main__":

    token = get_auth_token(DNAC_IP, DNAC_PORT, USERNAME, PASSWORD)

    devices_list = get_device_list(DNAC_IP, DNAC_PORT, token)
    pprint('Device data is: {}'.format(devices_list))

#   trying get_interface_list function without filter
#    interface_list = get_all_interfaces(DNAC_IP, DNAC_PORT, token)
#    print(interface_list)

#   trying to get the interface list using filter
#    device_id = 'de6477ad-22a2-4daa-9941-eb61cecefb34'
#    interface_list = get_all_interfaces(DNAC_IP, DNAC_PORT, token, device_id)
#    pprint(interface_list)

