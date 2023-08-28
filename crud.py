from typing import List
from sqlalchemy.orm import Session
from schema import ProductSchema, StoreSchema, InventorySchema
from model import Product, Store, Inventory

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
def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def get_product_by_pid(db: Session, pid: int):
    return db.query(Product).filter(Product.pid == pid).first()


def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Store).offset(skip).limit(limit).all()


def get_store_by_sid(db: Session, sid: int):
    return db.query(Store).filter(Store.sid == sid).first()


def get_inventory(db: Session, sid: int, pids: str):
    pids = pids.split(',')
    # Need to double-check if and is required here.
    return db.query(Inventory).filter(Inventory.sid == sid, Inventory.pid.in_(pids)).all()
#    return db.query(Inventory).filter(Store.sid == sid).filter(Product.pid in pids).all()


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
    if _inventory is not None:
        # Change inventory by delta.
        _inventory.quantity += inventory.quantity
    else:
        # Use delta as the absolute inventory as inventory doesn't exist
        _inventory = Inventory(sid=inventory.sid, pid=inventory.pid, quantity=inventory.quantity)
        db.add(_inventory)
    db.commit()
    db.refresh(_inventory)
    return _inventory


# Delete Operations
def delete_product():
    pass


def delete_store():
    pass


def delete_inventory():
    pass
