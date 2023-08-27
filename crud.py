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


def create_inventory(db: Session, inventory: InventorySchema):
    _inventory = Inventory(sid=inventory.sid, pid=inventory.pid, quantity=inventory.quantity)
    db.add(_inventory)
    db.commit()
    db.refresh(_inventory)
    return _inventory


# Read / Get Operations


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def get_product_by_pid():
    pass


def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Store).offset(skip).limit(limit).all()


def get_store_by_sid():
    pass


def get_inventory(db: Session, sid: int, pids: List[int]):
    # Need to double-check if and is required here.
    return db.query(Inventory).filter(Inventory.sid == sid, Inventory.pid.in_(pids)).all()
#    return db.query(Inventory).filter(Store.sid == sid).filter(Product.pid in pids).all()


# Update Operations


def update_product():
    pass


def update_store():
    pass


def update_inventory():
    pass


# Delete Operations


def delete_product():
    pass


def delete_store():
    pass


def delete_inventory():
    pass
