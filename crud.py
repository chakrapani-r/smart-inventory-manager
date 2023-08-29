from typing import List
from sqlalchemy.orm import Session
from schema import ProductSchema, StoreSchema, InventorySchema
from model import Product, Store, Inventory
import restock

# Create Operations
def create_product(db: Session, product: ProductSchema):
    _product = Product(name=product.name, description=product.description, price=product.price, supplier=product.supplier, category=product.category)
    db.add(_product)
    db.commit()
    db.refresh(_product)
    return _product


def create_store(db: Session, store: StoreSchema):
    _store = Store(name=store.name, address=store.address, city=store.city, manager=store.manager, manager_contact=store.manager_contact)
    db.add(_store)
    db.commit()
    db.refresh(_store)
    return _store

# Updates absolute inventory used to override or create new entry
def create_inventory(db: Session, inventory: InventorySchema):
    _inventory = db.query(Inventory).populate_existing().with_for_update(nowait=False, of=Inventory).filter(Inventory.sid == inventory.sid, Inventory.pid == inventory.pid).first()
    if _inventory is None:
        _inventory = Inventory(sid=inventory.sid, pid=inventory.pid, quantity=inventory.quantity)
        db.add(_inventory)
    else:
        _inventory.quantity = inventory.quantity
    db.commit()
    db.refresh(_inventory)
    return _inventory


# Read / Get Operations
def get_products(db: Session, skip: int = 0, limit: int = 100, pid_list: List[int] = None):
    if pid_list is None:
        return db.query(Product).offset(skip).limit(limit).all()
    else:
        # filter by given pids.
        return db.query(Product).filter(Product.pid.in_(pid_list)).offset(skip).limit(limit).all()


def get_product_by_pid(db: Session, pid: int):
    return db.query(Product).filter(Product.pid == pid).first()


def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Store).offset(skip).limit(limit).all()


def get_store_by_sid(db: Session, sid: int):
    return db.query(Store).filter(Store.sid == sid).first()


def get_inventory(db: Session, sid: int, pid_list: List[int]):
    # Need to double-check if and is required here.
    # product_details = db.query(Product).filter(Product.pid.in_(pids)).all()
    # product_details_tmp = db.query(Inventory).join(Product, Inventory.pid == Product.pid).all()
    # x = select([Inventory, Product]).select_from(Inventory.join(Product, Inventory.pid == Product.pid))
    # r = db.execute(x)
    # product_details_tmp = db.query(Inventory, Product).join(Inventory.pid == Product.pid).filter(Inventory.sid == sid, Inventory.pid.in_(pids), Product.pid.in_(pids)).all()
    # for p in r:
    #     print(p.__dict__)
    # print("----")
    inventory_details = db.query(Inventory).filter(Inventory.sid == sid, Inventory.pid.in_(pid_list)).all()
#    print(product_details.__dict__)
#     for product in product_details:
#         print(product.__dict__)
#     for _inv in inventory_details:
#         print(vars(_inv))

    return inventory_details
#    return db.query(Inventory).filter(Store.sid == sid).filter(Product.pid in pid_list).all()


# Update Operations
def update_product(db: Session, pid: int, product: ProductSchema):
    _product = get_product_by_pid(db=db, pid=pid)
    _product.name = product.name
    if product.description is not None:
        _product.description = product.description
    _product.price = product.price
    if product.category is not None:
        _product.category = product.category
    _product.supplier = product.supplier
    db.commit()
    db.refresh(_product)
    return _product


def update_store(db: Session, sid: int, store: StoreSchema):
    _store = get_store_by_sid(db=db, sid=sid)
    _store.name = store.name
    _store.manager = store.manager
    if store.city is not None:
        _store.city = store.city
    if store.address is not None:
        _store.address = store.address
    if store.manager_contact is not None:
        _store.manager_contact = store.manager_contact
    db.commit()
    db.refresh(_store)
    return _store


def update_inventory(db: Session, inventory: InventorySchema):
    _inventory = db.query(Inventory).populate_existing().with_for_update(nowait=False, of=Inventory).filter(Inventory.sid == inventory.sid, Inventory.pid == inventory.pid).first()
    prev_quantity = _inventory.quantity
    if _inventory is not None:
        # Change inventory by delta.
        _inventory.quantity += inventory.quantity
    else:
        # Use delta as the absolute inventory as inventory doesn't exist
        _inventory = Inventory(sid=inventory.sid, pid=inventory.pid, quantity=inventory.quantity)
        prev_quantity = 0
        db.add(_inventory)

    db.commit()
    db.refresh(_inventory)

    sid = _inventory.sid
    pid = _inventory.pid
    new_quantity = _inventory.quantity

    # Sending an inventory change log, ideally write this to a queue.
    _x = restock.inventory_change_event(db=db, sid=inventory.sid, pid=inventory.pid,
                                        current_quantity=new_quantity, prev_quantity=prev_quantity,
                                        delta=inventory.quantity)

    return {"sid": sid, "pid": pid, "quantity": new_quantity}


# Delete Operations
def delete_product():
    pass


def delete_store():
    pass


def delete_inventory():
    pass
