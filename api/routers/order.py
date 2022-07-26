from typing import List
from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse
from api.cruds.authentication import get_current_user
from api.schemas.user import UserSchema
from api.schemas.order import OrderList
from api.cruds.order import get_orders_by_user, create_order

router = APIRouter(tags=['Orders'], prefix='/orders')

@router.get('', response_model=List[OrderList])
async def list_orders(user: UserSchema = Depends(get_current_user)):
    orders = await get_orders_by_user(user)
    return JSONResponse(status_code=status.HTTP_200_OK, content=orders)

@router.post('')
async def create_orders(user: UserSchema = Depends(get_current_user)):
    await create_order(user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={'message': 'Create order.'})