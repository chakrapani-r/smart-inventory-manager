#import crud
import time

def inventory_change_event(sid: int, pid: int, current_quantity: int):
    # Log inventory change?
    # trigger ARS
    threshold = fetch_product_thresholds(sid, pid)
    if current_quantity < threshold["critical_threshold"]:
        # trigger purchase order with highest priority
        priority = 'critical'
        create_purchase_order(sid, pid, priority)
    elif current_quantity < threshold["threshold"]:
        # trigger purchase order with medium priority
        priority = 'normal'
        create_purchase_order(sid, pid, priority)

def fetch_product_thresholds(sid: int, pid: int):
    # thresholds can be set at a category level, product level and store-product level
    return {"threshold": 50, "critical_threshold": 10}

def create_purchase_order(sid: int, pid: int, priority: str):
    pass

def process_purchase_orders():
    # consider this is called when PO is fulfilled and GRN happens
    # update PO Status trigger GRN
    pass

def create_grn():
    pass
    # Create a GRN and trigger inventory update
    #update_inventory()

async def test_inventory_change_event(**kwargs):
    # print(kwargs['sid'])
    # print(kwargs['pid'])
    print("Within restock before sleep")
    with open('temp_async.txt', 'a') as f:
        f.write("Before sleep\n")
    time.sleep(30)
    with open('temp_async.txt', 'a') as f:
        f.write("Before sleep\n")

    print("Within restock After SLEEP")
