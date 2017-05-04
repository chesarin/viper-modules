#!/usr/bin/env python
import requests
import base64


def credentials_b64(username, password):
    combination = '%s:%s' % (username, password)
    combination_base64 = base64.b64encode(combination)
    return combination_base64


def get_connect_headers(b64_creds):
    headers = {'Accept': 'application/vnd.ve.v1.0+json',
               'Content-Type': 'application/json',
               'VE-SDK-API': b64_creds}
    return headers


def get_submit_headers(b64_creds):
    headers = {'Accept': 'application/vnd.ve.v1.0+json',
               'VE-SDK-API': b64_creds}
    return headers


def connect(host, username, password):
    creds = credentials_b64(username, password)
    headers = get_connect_headers(creds)
    try:
        r = requests.get(host, headers=headers, verify=False)
    except requests.ConnectionError:
        print 'ConnectionError'
    return r


def list_profiles(session, userid):
    host = 'https://172.28.21.250/php/vmprofiles.php'
    creds = credentials_b64(session, userid)
    headers = get_connect_headers(creds)
    try:
        r = requests.get(host, headers=headers, verify=False)
    except requests.ConnectionError:
        print 'ConnectionError'
    return r


def check_submission_status(submission):
    submission_result = submission.json()
    pass


def disconnect(host, session, userid):
    creds = credentials_b64(session, userid)
    headers = get_connect_headers(creds)
    try:
        r = requests.delete(host, headers=headers, verify=False)
    except requests.ConnectionError:
        print 'ConnectionError'
    return r


def submit_file(session, userid, filename):
    host = 'https://172.28.21.250/php/fileupload.php'
    creds = credentials_b64(session, userid)
    headers = get_submit_headers(creds)
    postdata = {
        'data': '{"data": {"xMode": 0, "overrideOS":1, "messageId": "", "vmProfileList": "13", "submitType": "0", "url": ""}}'}
    file_up = {'amas_filename': open(filename, 'r')}
    try:
        r = requests.post(host, postdata, files=file_up,
                          headers=headers, verify=False)
    except requests.ConnectionError:
        print 'ConnectionError'
    return r


# if __name__ == '__main__':
#     username = 'cvargas'
#     password = 'Mc@feeFTR123'
#     host = 'https://172.28.21.250/php/session.php'
#     filename = '/home/cesar/Downloads/malware/DoubleAgent/DoubleAgent_x64.exe'
#     connection_request = connect(host, username, password)
#     result = connection_request.json()
#     print result
#     # session = 'nv4aj53in9mf2i617j2nvqp8u4'
#     # userid = '46'
#     session = result['results']['session']
#     userid = result['results']['userId']
#     profiles = list_profiles(session, userid)
#     print profiles.json()
#     # filesubmission = submit_file(session, userid, filename)
#     disconnect_request = disconnect(host, session, userid)
#     print disconnect_request.json()
