import datetime
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from dbconnection import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
import crud
import grn
# from schema import ProductSchema, StoreSchema, InventorySchema
from schema import RequestProduct, RequestStore, RequestInventory, RequestBulkInventory, Response, User, UserLogin
from auth_bearer import JWTBearer
from auth import signJWT
import concurrency_test

from collections import defaultdict

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/product', dependencies=[Depends(JWTBearer())], tags=["Product"])
async def create_product(request: RequestProduct, db: Session = Depends(get_db)):
    _product = crud.create_product(db, request.parameter)
    return Response(code="200", status="ok", message="Success", result=_product).model_dump(exclude_none=True)


@router.put('/product', dependencies=[Depends(JWTBearer())], tags=["Product"])
async def update_product(request: RequestProduct, db: Session = Depends(get_db)):
    _product = crud.update_product(db=db, pid=request.parameter.pid, product=request.parameter)
    return Response(code="200", status="ok", message="Success", result=_product).model_dump(exclude_none=True)


@router.post('/store', dependencies=[Depends(JWTBearer())], tags=["Store"])
async def create_store(request: RequestStore, db: Session = Depends(get_db)):
    _store = crud.create_store(db, request.parameter)
    return Response(code="200", status="ok", message="Success", result=_store).model_dump(exclude_none=True)


@router.put('/store', dependencies=[Depends(JWTBearer())], tags=["Store"])
async def update_store(request: RequestStore, db: Session = Depends(get_db)):
    _store = crud.update_store(db=db, sid=request.parameter.sid, store=request.parameter)
    return Response(code="200", status="ok", message="Success", result=_store).model_dump(exclude_none=True)


@router.post('/inventory', tags=["Inventory"])
async def create_inventory(request: RequestInventory, db: Session = Depends(get_db)):
    _inventory = crud.create_inventory(db, request.parameter)
    return Response(code="200", status="ok", message="Success", result=_inventory).model_dump(exclude_none=True)

@router.put('/inventory', tags=["Inventory"])
async def update_inventory(request: RequestInventory, db: Session = Depends(get_db)):
    _inventory = crud.update_inventory(db, request.parameter)
    return Response(code="200", status="ok", message="Success", result=_inventory).model_dump(exclude_none=True)


@router.get('/product', dependencies=[Depends(JWTBearer())], tags=["Product"])
async def get_product(offset: int = 0, db: Session = Depends(get_db)):
    limit = 100
    _products = crud.get_products(db=db, skip=offset, limit=limit)
    return Response(code="200", status="ok", message="Success", result=_products).model_dump(exclude_none=True)


@router.get('/product/{pid}', dependencies=[Depends(JWTBearer())], tags=["Product"])
async def get_product_by_pid(pid: Annotated[int, Path(title="The PID of the product to get", ge=1)], db: Session = Depends(get_db)):
    _product = crud.get_product_by_pid(db, pid)
    return Response(code="200", status="ok", message="Success", result=_product).model_dump(exclude_none=True)


@router.get('/store', dependencies=[Depends(JWTBearer())], tags=["Store"])
async def get_store(offset: int = 0, db: Session = Depends(get_db)):
    limit = 100
    _stores = crud.get_stores(db, offset, limit)
    return Response(code="200", status="ok", message="Success", result=_stores).model_dump(exclude_none=True)


@router.get('/store/{sid}', dependencies=[Depends(JWTBearer())], tags=["Store"])
async def get_store_by_sid(sid: Annotated[int, Path(title="The SID of the store to get", ge=1)], db: Session = Depends(get_db)):
    limit = 100
    _store = crud.get_store_by_sid(db, sid)
    return Response(code="200", status="ok", message="Success", result=_store).model_dump(exclude_none=True)


# pids are expected to be csv
@router.get('/inventory', tags=["Inventory"])
async def get_inventory(sid: int, pids: str, db: Session = Depends(get_db)):
    # pids = pids.split(',')
    pid_list = list(map(int, pids.split(',')))
    _inv = crud.get_inventory(db, sid, pid_list)
    _products = crud.get_products(db=db, skip=0, limit=1000, pid_list=pid_list)

    # r = _inv + _products
    # result = defaultdict(dict)
    # # @TODO fix this
    # for l in (_inv, _products):
    #     for elem in l:
    #         elem = elem.__dict__
    #         result[elem['pid']].update(elem)
    # result = list(result.values())

    _result = [{**u.__dict__, **v.__dict__} for u, v in zip(_inv, _products)]
    # return Response(code="200", status="ok", message="Success", result=_result).dict(exclude_none=True)
    return Response(code="200", status="ok", message="Success", result=_result).model_dump(exclude_none=True)

@router.post("/user/signup", tags=["user"])
async def create_user(user: User):
    # add user to the user database.
    return signJWT(user.email)

@router.post("/user/login", tags=["user"])
async def user_login(user: UserLogin):
    if validate_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }

def validate_user(data: UserLogin):
    # Actual validation can reside here
    # for now returning true for any non-empty password
    if data.password:
        return True
    return False

# This should be triggered every few mins
@router.get("/cron/purchase-orders", include_in_schema=False)
async def cron(db: Session = Depends(get_db)):
    grn.process_purchase_orders(db)
    _time = datetime.datetime.now()
    print(f"Purchase Orders cron ran succesfully @{_time}")
    return {
        "message": f"Purchase orders cron run completed @ {_time}"
    }

# This shall be triggered as per the lead time..once every few hours or hourly
@router.get("/cron/sales-trends", include_in_schema=False)
async def cron(db: Session = Depends(get_db)):
    grn.calculate_sales_trends(db)
    _time = datetime.datetime.now()
    print(f"Sales Trends cron ran succesfully @{_time}")
    return {
        "message": f"Sales trends cron run completed @ {_time}"
    }

# Test Url
@router.get("/test", include_in_schema=False)
async def cron(db: Session = Depends(get_db)):

    res = concurrency_test.run_concurrency_test()

    _time = datetime.datetime.now()
    # print(f"Concurrency test done @{_time}")
    return {
        "message": f"{res} @ {_time}"
    }
