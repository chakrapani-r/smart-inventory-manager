from typing import Generic, Optional, TypeVar, List
from pydantic import BaseModel, Field

T = TypeVar('T')


class ProductSchema(BaseModel):
    pid: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    supplier: str
    category: Optional[str] = None

    class Config:
        from_attributes = True


class RequestProduct(BaseModel):
    parameter: ProductSchema = Field(...)


class StoreSchema(BaseModel):
    sid: Optional[int] = None
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    manager: str
    manager_contact: Optional[str] = None

    class Config:
        from_attributes = True


class RequestStore(BaseModel):
    parameter: StoreSchema = Field(...)


class InventorySchema(BaseModel):
    sid: int
    pid: int
    quantity: int

    class Config:
        from_attributes = True


class RequestInventory(BaseModel):
    parameter: InventorySchema = Field(...)


class RequestBulkInventory(BaseModel):
    sid: int
    pids: str


class Response(BaseModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T] = None
