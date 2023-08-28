from sqlalchemy import Column, String, Integer, Float, ForeignKey, PrimaryKeyConstraint, DateTime, TIMESTAMP
#from geoalchemy2 import Geometry
from dbconnection import Base
from pydantic import Field, EmailStr

class Product(Base):
    __tablename__ = 'products'

    pid = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    supplier = Column(String)
    category = Column(String)


class Store(Base):
    __tablename__ = "stores"

    sid = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    city = Column(String)
#    location = Column(Geometry(geometry_type='POINT'))
    manager = Column(String)
    manager_contact = Column(String)


class Inventory(Base):
    __tablename__ = "inventory"

    sid = Column(Integer, ForeignKey('stores.sid'), nullable=False)
    pid = Column(Integer, ForeignKey('products.pid'), nullable=False)
    quantity = Column(Integer, nullable=False)
    __table_args__ = (
         PrimaryKeyConstraint(sid, pid),
         {}
    )

class PurchaseOrder(Base):
    __tablename__ = "purchase_order"

    po_id = Column(Integer, primary_key=True)
    sid = Column(Integer, ForeignKey('stores.sid'), nullable=False)
    pid = Column(Integer, ForeignKey('products.pid'), nullable=False)
    quantity = Column(Integer, nullable=False)
    created = Column(DateTime)
    fulfilled = Column(DateTime, nullable=True)
    vendor = Column(Integer, nullable=True)
    status = Column(String, nullable=True)
    grn_id = Column(Integer, nullable=True)

# Ideally this belongs in a timeseries or nosql db , putting it in pgsql due to limited time.
class InventoryLogs(Base):
    __tablename__ = "inventory_logs"

    log_id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP)
    pid = Column(Integer, ForeignKey('products.pid'), nullable=False)
    sid = Column(Integer, ForeignKey('stores.sid'), nullable=False)
    quantity_change = Column(Integer)
    previous_quantity = Column(Integer)
    new_quantity = Column(Integer)
    action = Column(String, nullable=True)

class AggregatedSales(Base):
    __tablename__ = "aggregated_sales"
    pid = Column(Integer, ForeignKey('products.pid'), nullable=False)
    sid = Column(Integer, ForeignKey('stores.sid'), nullable=False)
    avg_sales = Column(Integer, nullable=False)
    max_sales = Column(Integer, nullable=False)
    lead_time = Column(Integer, nullable=False)
    max_lead_time = Column(Integer, nullable=False)
    updated = Column(TIMESTAMP)
    __table_args__ = (
         PrimaryKeyConstraint(sid, pid),
         {}
    )

# class POStatus(str, Enum):
#     created = "created",
#     approved = "approved",
#     delayed = "delayed"
#     closed = "closed"


# class User(Base):
#     name: str = Field(...)
#     email: EmailStr = Field(...)
#     password: str = Field(...)
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "Chakrapani R",
#                 "email": "chakrapani.reddivari@gmail.com",
#                 "password": "mediumpassword"
#             }
#         }
# class UserLogin(Base):
#     email: EmailStr = Field(...)
#     password: str = Field(...)
