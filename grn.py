import crud
import datetime
from datetime import timedelta
from model import Inventory, PurchaseOrder, InventoryLogs
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from decouple import config

# This is not the most efficient approach, we will limit 1000 per cron run for now
# consider this is called when PO is fulfilled and GRN happens
# update PO Status trigger GRN
def process_purchase_orders(db: Session):
    _res = db.query(PurchaseOrder).filter(or_(PurchaseOrder.status == "created", PurchaseOrder.status == "approved")).limit(1000).all()
    time_delay = int(config("time_delay_for_po"))
    for po in _res:
        inventory = Inventory(sid=po.sid, pid=po.pid, quantity=po.quantity)
        if po.status == "approved":
            # process immediately
            trigger_inventory_update(db, inventory, po)
        elif po.created < (datetime.datetime.now() - timedelta(minutes=time_delay)):
            # process purchase order if it has crossed time delay.
            # so this is equivalent to auto approval after time delay.
            trigger_inventory_update(db, inventory, po)
            #
            # try:
            #     _r = crud.update_inventory(db, inventory)
            #     po.fulfilled = datetime.datetime.now()
            #     po.status = "closed"
            #     db.commit()
            #     db.refresh(po)
            # except:
            #     print(f"Failed to process PO {po.po_id}")

def trigger_inventory_update(db: Session, inventory: Inventory, po: PurchaseOrder):
        try:
            _r = crud.update_inventory(db, inventory)
            po.fulfilled = datetime.datetime.now()
            po.status = "closed"
            db.commit()
            db.refresh(po)
        except:
            print(f"Failed to process PO {po.po_id}")

def calculate_sales_trends(db):
    interval = int(config("sales_trend_interval"))
    # interval = 1.25
    t = datetime.datetime.now() - timedelta(hours=interval)
    distinct_combinations = (db.query(InventoryLogs.pid, InventoryLogs.sid, func.sum(InventoryLogs.quantity_change)).filter(InventoryLogs.timestamp >= t, InventoryLogs.quantity_change < 0).group_by(InventoryLogs.pid, InventoryLogs.sid).all())
    sales_threshold = config("sales_trend_threshold")
    for pid, sid, delta in distinct_combinations:
        delta *= -1
        if delta > sales_threshold:
            # Trigger replenishment because of fast moving sku
            # create a PO with high priority and fastest restock.
            create_priority_purchase_order(db, sid, pid, delta)

    return {"message": "Cron run okay"}
    # time taken to restock = 0
    # hourly trend, weekly trend
    # trend orders vs product - try to get a multiplier last week last day
    # optimize for the cost restocking

def create_priority_purchase_order(db, sid: int, pid: int, quantity: int):
    #quantity = calculate_quantity_to_purchase(db, pid, sid, current_quantity)
    if quantity > 0:
        # create PO
        created = datetime.datetime.now()
        purchase_order = PurchaseOrder(sid=sid, pid=pid, quantity=quantity, created=created, status='approved')
        db.add(purchase_order)
        db.commit()
    return
