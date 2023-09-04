import datetime
from datetime import timedelta
import random
import math
import time
from model import PurchaseOrder, InventoryLogs, AggregatedSales
from sqlalchemy.orm import Session
from decouple import config

def inventory_change_event(db: Session, sid: int, pid: int, current_quantity: int, prev_quantity=int, delta=int):
    # Log inventory change
    write_to_inventory_log(db, sid, pid, current_quantity, prev_quantity, delta)
    # trigger ARS
    threshold = fetch_product_thresholds(sid, pid)
    if current_quantity < threshold["critical_threshold"]:
        # trigger purchase order with highest priority
        priority = 'critical'
        create_purchase_order(db, sid, pid, current_quantity, priority)
    elif current_quantity < threshold["threshold"]:
        # trigger purchase order with medium priority
        priority = 'normal'
        create_purchase_order(db, sid, pid, current_quantity, priority)

# Ideally this shall be done via queue and to a more suitable database
def write_to_inventory_log(db: Session, sid: int, pid: int, current_quantity: int, prev_quantity=int, delta=int):
    log = InventoryLogs(sid=sid, pid=pid, quantity_change=delta, previous_quantity=prev_quantity,
                        new_quantity=current_quantity, action="update", timestamp=datetime.datetime.now())
    db.add(log)
    db.commit()
    return

def fetch_product_thresholds(sid: int, pid: int):
    # thresholds can be set at a category level, product level and store-product level
    # for now using default values
    threshold = int(config("threshold"))
    critical_threshold = int(config("critical_threshold"))
    return {"threshold": threshold, "critical_threshold": critical_threshold}

def create_purchase_order(db, sid: int, pid: int, current_quantity: int, priority: str):
    quantity = calculate_quantity_to_purchase(db, pid, sid, current_quantity)
    if quantity > 0:
        # create PO
        created = datetime.datetime.now()
        purchase_order = PurchaseOrder(sid=sid, pid=pid, quantity=quantity, created=created, status='created')
        db.add(purchase_order)
        db.commit()
    return

# Calculate the quantity needed to restock for a given SKU at a given store.
def calculate_quantity_to_purchase(db: Session, pid: int, sid: int, current_quantity: int):
    # multiples of lead time. i.e this will be 4 if we order once every 4 hrs & leadtime =1hr
    # delay as the multiple of lead time.
    replenishment_forced_delay = int(config('replenishment_forced_delay'))
    # Avg lead time. get from historical PO fulfilment set to 1hr for the scope of this project

    trends = get_trends_data(db, sid, pid)
    lead_time = trends["lead_time"]
    max_lead_time = trends["max_lead_time"]
    avg_sale_per_lead_time = trends["avg"]
    max_sale_per_lead_time = trends["max"]

    safe_stock = (max_lead_time * max_sale_per_lead_time) - (lead_time * avg_sale_per_lead_time)
    buffer = safe_stock

    projected_sale_per_lead_time = avg_sale_per_lead_time
    # ideally get the actual remaining time.
    remaining_time_in_current_lead_time_window = random.randint(1, 10)/10
    projected_sale_for_current_lead_time = math.ceil(avg_sale_per_lead_time * remaining_time_in_current_lead_time_window)
    projected_sale_for_current_window = projected_sale_for_current_lead_time + (projected_sale_per_lead_time * (replenishment_forced_delay -1))
    # TODO get already placed purchase order quantity
    existing_unfulfilled_order_qty = get_pending_purchase_order_quantity(db, sid, pid)

    inventory_at_end_of_current_window = max(0, current_quantity - projected_sale_for_current_window)
    # we can't do much for current window, so plan for next window.
    qty_needed_next_window = lead_time * projected_sale_per_lead_time * replenishment_forced_delay

    qty_needed = qty_needed_next_window + buffer - existing_unfulfilled_order_qty

    inventory_diff = 0
    if qty_needed > inventory_at_end_of_current_window:
        inventory_diff = qty_needed - inventory_at_end_of_current_window

    return inventory_diff

def get_trends_data(db: Session, sid: int, pid: int):
    sales = db.query(AggregatedSales).populate_existing().with_for_update(nowait=False, of=AggregatedSales)\
        .filter(AggregatedSales.sid == sid, AggregatedSales.pid == pid).first()
    lead_time = int(config("lead_time"))
    max_lead_time = int(config("max_lead_time"))
    if sales is None:
        # populating random sales data. ideally this should be calculated
        avg_sales = random.randint(5, 50)
        max_sales = random.randint(avg_sales, 200)
        sales = AggregatedSales(sid=sid, pid=pid, avg_sales=avg_sales, max_sales=max_sales, lead_time=lead_time, max_lead_time=max_lead_time)
        db.add(sales)
        db.commit()
        db.refresh(sales)
    return {"avg": sales.avg_sales, "max": sales.max_sales, "lead_time": lead_time, "max_lead_time": max_lead_time}

def get_pending_purchase_order_quantity(db: Session, sid: int, pid: int):
    purchase_orders = db.query(PurchaseOrder).filter(PurchaseOrder.status == "created",
                                   PurchaseOrder.sid == sid, PurchaseOrder.pid == pid).all()
    qty = 0
    if purchase_orders is not None:
        for _po in purchase_orders:
            qty += _po.quantity
    return qty
