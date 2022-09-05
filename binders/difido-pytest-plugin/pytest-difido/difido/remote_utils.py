'''
Created on Aug 10, 2017

@author: Itai Agmon
'''

import json

from . import config
from http import client
import requests


def __generate_base_url():
    url = f"http://{config.host}:{str(config.port)}"
    return url


def prepare_remote_execution(details):
    res = send_request(method="POST", url=f"{__generate_base_url()}/api/executions", data=to_content(details), headers={"Content-Type": "application/json"})
    return res.content.decode()


def add_machine(execution_id, machine):
    res = send_request("POST", f"{__generate_base_url()}/api/executions/{execution_id}/machines/", to_content(machine), {"Content-Type": "application/json"})
    return res.content.decode()


def update_machine(execution_id, machine_id, machine):
    send_request("PUT", f"{__generate_base_url()}/api/executions/{execution_id}/machines/{machine_id}", to_content(machine), {"Content-Type": "application/json"})


def add_test_details(execution_id, test_details):
    send_request("POST", f"{__generate_base_url()}/api/executions/{execution_id}/details", to_content(test_details), {"Content-Type": "application/json"})


def end_execution(execution_id):
    send_request("PUT", f"{__generate_base_url()}/api/executions/{execution_id}?active=false", "", {"Content-Type": "application/json"})


def add_file(execution_id, uid, file):
    host = config.host
    port = config.port
    files = {"file": open(file, "rb")}
    try:
        res = requests.request_timeout("POST", f"{__generate_base_url()}/api/executions/{execution_id}/details/{uid}/file/", files=files, timeout=20)
        # print("finished add_file")
        if res is not None:
            if res.status_code != 200:
                print(res.reason)

    except Exception as e:
        print('Error during file upload: ' + str(e))


def to_content(obj):
    dicts = obj.dict()
    content = json.dumps(dicts)
    return content


def send_request(method, url, data, headers):
    res = requests.request(method, url=url, data=data, headers=headers, timeout=20)
    try:
        if res.status_code != 200 and res.status_code != 204:
            raise Exception("Error in response. error code " + str(res.status))
    except Exception as e:
        # print("method " + str(method))
        # print("url " + str(url))
        # print("data " + str(data))
        # print("headers " + str(headers))
        # print(res.args)
        pass
    return res


def get_connection():
    return client.HTTPSConnection(host=config.host, port=config.port, timeout=10)
