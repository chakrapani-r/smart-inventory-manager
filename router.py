from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List
from dbconnection import SessionLocal
from sqlalchemy.orm import Session
import crud
from schema import ProductSchema, StoreSchema, InventorySchema
from schema import RequestProduct, RequestStore, RequestInventory, RequestBulkInventory, Response

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @router.post('/product/create', response_model=ProductSchema)
@router.post('/product/create')
def create_product(request: RequestProduct, db: Session = Depends(get_db)):
    _product = crud.create_product(db, request.parameter)
    return Response(code="200", status="ok", message="Success", result=_product).dict(exclude_none=True)


# @router.post('/store/create', response_model=StoreSchema)
@router.post('/store/create')
def create_store(request: RequestStore, db: Session = Depends(get_db)):
    _store = crud.create_store(db, request.parameter)
    return Response(code="200", status="ok", message="Success", result=_store).dict(exclude_none=True)


# @router.post('/inventory/create', response_model=InventorySchema)
@router.post('/inventory/create')
def create_inventory(request: RequestInventory, db: Session = Depends(get_db)):
    _inventory = crud.create_inventory(db, request.parameter)
    return Response(code="200", status="ok", message="Success", result=_inventory).dict(exclude_none=True)


# @router.get('/product', response_model=List[ProductSchema])
@router.get('/product')
def get_product(db: Session = Depends(get_db)):
    _products = crud.get_products(db, 0, 100)
    return Response(code="200", status="ok", message="Success", result=_products).dict(exclude_none=True)


# @router.get('/store', response_model=List[StoreSchema])
@router.get('/store')
def get_store(db: Session = Depends(get_db)):
    _stores = crud.get_stores(db, 0, 100)
    return Response(code="200", status="ok", message="Success", result=_stores).dict(exclude_none=True)


# @router.get('/inventory', response_model=List[InventorySchema])
@router.post('/inventory')
def get_inventory(request: RequestBulkInventory, db: Session = Depends(get_db)):
    _inv = crud.get_inventory(db, request.sid, request.pids)
    return Response(code="200", status="ok", message="Success", result=_inv).dict(exclude_none=True)

