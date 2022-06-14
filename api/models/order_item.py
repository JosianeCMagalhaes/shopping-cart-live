from typing import Optional
from pydantic import BaseModel
from api.models.order import OrderSchema
from api.models.product import ProductSchema

class OrderItemSchema(BaseModel):
    order: OrderSchema
    product: ProductSchema
    
class OrderItemSchemaUpdate(BaseModel):
    order: Optional[OrderSchema]
    product: Optional[ProductSchema]

class OrderList(OrderItemSchema):
    _id: str
    order: OrderItemSchema

    