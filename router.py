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


@router.post('/product')
def create_product(request: RequestProduct, db: Session = Depends(get_db)):
    _product = crud.create_product(db, request.parameter)
    return Response(code="200", status="ok", message="Success", result=_product).dict(exclude_none=True)


@router.put('/product')
def create_product(request: RequestProduct, db: Session = Depends(get_db)):
    _product = crud.update_product(db=db, pid=request.parameter.pid, product=request.parameter)
    return Response(code="200", status="ok", message="Success", result=_product).dict(exclude_none=True)


@router.post('/store')
def create_store(request: RequestStore, db: Session = Depends(get_db)):
    _store = crud.create_store(db, request.parameter)
    return Response(code="200", status="ok", message="Success", result=_store).dict(exclude_none=True)


@router.put('/store')
def update_store(request: RequestStore, db: Session = Depends(get_db)):
    _store = crud.update_store(db=db, sid=request.parameter.sid, store=request.parameter)
    return Response(code="200", status="ok", message="Success", result=_store).dict(exclude_none=True)


@router.post('/inventory')
def create_inventory(request: RequestInventory, db: Session = Depends(get_db)):
    _inventory = crud.create_inventory(db, request.parameter)
    return Response(code="200", status="ok", message="Success", result=_inventory).dict(exclude_none=True)

@router.put('/inventory')
def update_inventory(request: RequestInventory, db: Session = Depends(get_db)):
    _inventory = crud.update_inventory(db, request.parameter)
    return Response(code="200", status="ok", message="Success", result=_inventory).dict(exclude_none=True)


@router.get('/product')
def get_product(offset: int = 0, db: Session = Depends(get_db)):
    limit = 100
    _products = crud.get_products(db, offset, limit)
    return Response(code="200", status="ok", message="Success", result=_products).dict(exclude_none=True)


@router.get('/product/{pid}')
def get_product_by_pid(pid: int, db: Session = Depends(get_db)):
    _product = crud.get_product_by_pid(db, pid)
    return Response(code="200", status="ok", message="Success", result=_product).dict(exclude_none=True)


@router.get('/store')
def get_store(offset: int = 0, db: Session = Depends(get_db)):
    limit = 100
    _stores = crud.get_stores(db, offset, limit)
    return Response(code="200", status="ok", message="Success", result=_stores).dict(exclude_none=True)


@router.get('/store/{sid}')
def get_store_by_sid(sid: int, db: Session = Depends(get_db)):
    limit = 100
    _store = crud.get_store_by_sid(db, sid)
    return Response(code="200", status="ok", message="Success", result=_store).dict(exclude_none=True)


# pids are expected to be csv
@router.get('/inventory')
def get_inventory(sid: int, pids: str, db: Session = Depends(get_db)):
    _inv = crud.get_inventory(db, sid, pids)
    return Response(code="200", status="ok", message="Success", result=_inv).dict(exclude_none=True)

