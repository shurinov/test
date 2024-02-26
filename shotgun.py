import time
import requests
from jsonrpcclient import Error, Ok, parse, request, request_json


def jsonrpc_request(url:str, r_type:str, params:dict, timeout:int=10) -> dict:
    # assembly rpc request
    r = request(r_type, params)
    try:
        response = requests.post(url, json=r, timeout=timeout)
    except requests.ReadTimeout as err:
        msg = f'Jsonrpc error occurred: {err}'
        print(msg)
        return dict(code=-1, info=msg)
    except requests.ConnectionError as err:
        msg = f'Jsonrpc error occurred: {err}'
        print(msg)
        return dict(code=-2, info=msg)

    parsed = parse(response.json())
    if isinstance(parsed, Ok):
        #'code' : 0 - ok
        #'code' : 1 - some problems, see 'info'
        return parsed.result.get('response', 
            dict(code=-3, info='Response field is not exist'))
    else:
        msg = f"jsonrpc parsed problem: {parsed.message}"
        print(msg)
        return dict(code=-4, info=msg)
    

def req_nam_val_comission(nam_addr:str) -> tuple:
    path = f"/vp/pos/validator/commission/{nam_addr}"
    return ("abci_query", {"path":path,"data": "", "prove": False})


def get_val_commission_rate(url:str, tnam_addr:str) -> int:
    req = req_nam_val_comission(tnam_addr)
    data = jsonrpc_request(url, req[0], req[1])
    return data


def det_last_height(url:str) -> int:
    resp = requests.get(f"{url}/status")
    data = resp.json()
    return data['result']['sync_info']['latest_block_height']


node_url = 'http://localhost:26657'


h = det_last_height(node_url)
print(f"Height: {h}")

data = get_val_commission_rate(node_url,'tnam1q8hu2fww5t6xqffux6uydq9v7m2jl0wsavpu7vv8')
print(data)
print("All good")


h = det_last_height(node_url)
print(f"Height: {h}")

# shot
data = get_val_commission_rate(node_url, 0)
print(data)

time.sleep(10)

h = det_last_height(node_url)
print(f"Height: {h}")

time.sleep(20)

h = det_last_height(node_url)
print(f"Height: {h}")

time.sleep(30)

h = det_last_height(node_url)
print(f"Height: {h}")

print("WTF?")
