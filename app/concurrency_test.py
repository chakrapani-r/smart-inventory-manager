import random

import requests
import concurrent.futures


def send_test_request(url, payload):
    # print(payload)
    _response = requests.put(url, json=payload)
    # print(_response.__dict__)

def run_concurrency_test():
    url_endpoint = "http://139.59.50.113/inventory"
    sample_payload = [{
        "parameter": {
            "sid": 14,
            "pid": 1,
            "quantity": -5
        }
    },
        {
        "parameter": {
            "sid": 14,
            "pid": 1,
            "quantity": 2
        }
    },{
        "parameter": {
            "sid": 14,
            "pid": 1,
            "quantity": -1
        }
    },
        {
        "parameter": {
            "sid": 14,
            "pid": 1,
            "quantity": 0
        }
    },
        {
        "parameter": {
            "sid": 14,
            "pid": 1,
            "quantity": -3
        }
    }
    ]
    get_payload = "?sid=14&pids=1"
    response = requests.get(url_endpoint + get_payload)
    print(f"======response={response.json()['result']}======")
    delta = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for _ in range(25):
            pl = random.choice(sample_payload)
            delta += pl['parameter']['quantity']
            executor.submit(send_test_request, url_endpoint, payload=pl)
    prev_quantity = response.json()['result'][0]['quantity']
    new_response = requests.get(url_endpoint + get_payload)
    new_quantity = new_response.json()['result'][0]['quantity']

    print(f"======prev quantity={prev_quantity}======")
    print(f"======delta={delta}======")
    print(f"======new quantity={new_quantity}======")

    if prev_quantity + delta == new_quantity:
        return "Concurrency Test passed!"
    else:
        return "Concurrency Test failed!"


# run_concurrency_test()
