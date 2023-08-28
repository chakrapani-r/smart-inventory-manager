from fastapi import APIRouter, Depends, HTTPException, Path, Query
from dbconnection import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import Field
import crud
# from schema import ProductSchema, StoreSchema, InventorySchema
from schema import RequestProduct, RequestStore, RequestInventory, RequestBulkInventory, Response

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/product')
async def create_product(request: RequestProduct, db: Session = Depends(get_db)):
    _product = crud.create_product(db, request.parameter)
    return Response(code="200", status="ok", message="Success", result=_product).dict(exclude_none=True)


@router.put('/product')
async def update_product(request: RequestProduct, db: Session = Depends(get_db)):
    _product = crud.update_product(db=db, pid=request.parameter.pid, product=request.parameter)
    return Response(code="200", status="ok", message="Success", result=_product).dict(exclude_none=True)


@router.post('/store')
async def create_store(request: RequestStore, db: Session = Depends(get_db)):
    _store = crud.create_store(db, request.parameter)
    return Response(code="200", status="ok", message="Success", result=_store).dict(exclude_none=True)


@router.put('/store')
async def update_store(request: RequestStore, db: Session = Depends(get_db)):
    _store = crud.update_store(db=db, sid=request.parameter.sid, store=request.parameter)
    return Response(code="200", status="ok", message="Success", result=_store).dict(exclude_none=True)


@router.post('/inventory')
async def create_inventory(request: RequestInventory, db: Session = Depends(get_db)):
    _inventory = crud.create_inventory(db, request.parameter)
    return Response(code="200", status="ok", message="Success", result=_inventory).dict(exclude_none=True)

@router.put('/inventory')
async def update_inventory(request: RequestInventory, db: Session = Depends(get_db)):
    _inventory = crud.update_inventory(db, request.parameter)
    return Response(code="200", status="ok", message="Success", result=_inventory).dict(exclude_none=True)


@router.get('/product')
async def get_product(offset: int = 0, db: Session = Depends(get_db)):
    limit = 100
    _products = crud.get_products(db=db, skip=offset, limit=limit)
    return Response(code="200", status="ok", message="Success", result=_products).dict(exclude_none=True)


@router.get('/product/{pid}')
async def get_product_by_pid(pid: Annotated[int, Path(title="The PID of the product to get", ge=1)], db: Session = Depends(get_db)):
    _product = crud.get_product_by_pid(db, pid)
    return Response(code="200", status="ok", message="Success", result=_product).dict(exclude_none=True)


@router.get('/store')
async def get_store(offset: int = 0, db: Session = Depends(get_db)):
    limit = 100
    _stores = crud.get_stores(db, offset, limit)
    return Response(code="200", status="ok", message="Success", result=_stores).dict(exclude_none=True)


@router.get('/store/{sid}')
async def get_store_by_sid(sid: Annotated[int, Path(title="The SID of the store to get", ge=1)], db: Session = Depends(get_db)):
    limit = 100
    _store = crud.get_store_by_sid(db, sid)
    return Response(code="200", status="ok", message="Success", result=_store).dict(exclude_none=True)


# pids are expected to be csv
@router.get('/inventory')
async def get_inventory(sid: int, pids: str, db: Session = Depends(get_db)):
    _inv = crud.get_inventory(db, sid, pids)
    return Response(code="200", status="ok", message="Success", result=_inv).dict(exclude_none=True)
