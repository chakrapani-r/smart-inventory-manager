#import crud
import random
import math
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
    # Actual restocking happens here
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

# time taken to restock = 0
# frequency =1,2 not immediately
# hourly trend, weekly trend
# trend orders vs product - try to get a multiplier last week last day
# optimize for the cost restocking

# Calculate the quantity needed to restock for a given SKU at a given store.
def calculate_quantity_to_purchase(pid: int, sid: int):
    # multiples of lead time. i.e this will be 4 if we order once every 4 hrs & leadtime =1hr
    replenishment_frequency = 1
    # Avg lead time. get from historical PO fulfilment set to 1hr for the scope of this project
    lead_time = 1
    # TODO get from historical PO fulfilment
    max_lead_time = 2
    # TODO get from sales
    avg_sale_per_lead_time = 10
    # TODO get from sales
    max_sale_per_lead_time = 20

    safe_stock = (max_lead_time * max_sale_per_lead_time) - (lead_time * avg_sale_per_lead_time)
    buffer = safe_stock

    projected_sale_per_lead_time = avg_sale_per_lead_time
    # ideally get the actual remaining time.
    remaining_time_in_current_lead_time_window = random.randint(1,10)/10
    projected_sale_for_current_lead_time = math.ceil(avg_sale_per_lead_time * remaining_time_in_current_lead_time_window)
    projected_sale_for_current_window = projected_sale_for_current_lead_time + (projected_sale_per_lead_time * (replenishment_frequency -1))
    # TODO get already placed purchase order quantity
    existing_unfulfilled_order_qty = 1
    # TODO current inventory for the product
    current_inventory = 1
    inventory_at_end_of_current_window = max(0, current_inventory - projected_sale_for_current_window)
    # we can't do much for current window, so plan for next window.
    qty_needed_next_window = lead_time * projected_sale_per_lead_time * replenishment_frequency

    qty_needed = qty_needed_next_window + buffer - existing_unfulfilled_order_qty

    inventory_diff = 0
    if qty_needed > inventory_at_end_of_current_window:
        inventory_diff = qty_needed - inventory_at_end_of_current_window

    return inventory_diff
