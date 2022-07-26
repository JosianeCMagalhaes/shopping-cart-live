from typing import List, Optional
from pydantic import BaseModel

class CartItemsSchema(BaseModel):
    user_id: str
    product_id: str
    product_image: str
    product_price: str
    product_quantity: str
    row_id: Optional[str]

class CartSchema(BaseModel):
    product_id: str
    quantity: int
    
class CartTotalSchema(CartSchema):
    total_price: float
    items: List[CartItemsSchema] = []

    class Config:
        orm_mode = True
    
    