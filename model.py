from sqlalchemy import Column, String, Integer, Float, ForeignKey, PrimaryKeyConstraint
#from geoalchemy2 import Geometry
from dbconnection import Base


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

