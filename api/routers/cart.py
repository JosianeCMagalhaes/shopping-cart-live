from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse
from decimal import Decimal
from api.cruds.cart import delete_all_carts, delete_cart, get_carts, add_cart
from api.cruds.product import get_product
from api.schemas.cart import CartItemsSchema, CartSchema
from api.schemas.user import UserList
from api.cruds.authentication import get_current_user

router = APIRouter(tags=['Carts'], prefix='/carts')

@router.post('')
async def add_to_cart(cart: CartSchema, user: UserList = Depends(get_current_user)):
    product = await get_product(cart.product_id)
    cart_items = CartItemsSchema(user_id=str(user['_id']),
                                 product_id=product['_id'],
                                 product_image=str(product['image']),
                                 product_price=str(Decimal(product['price']) * cart.quantity),
                                 product_quantity=cart.quantity)

    add_cart(cart_items)
    return JSONResponse(status_code=status.HTTP_200_OK, content={'message': 'Add to cart'})

@router.get('')
def carts(user: UserList = Depends(get_current_user)):
    carts = get_carts(user)
    return JSONResponse(status_code=status.HTTP_200_OK, content=carts)


@router.delete('')
def clear_cart(user: UserList = Depends(get_current_user)):
    delete_all_carts(str(user['_id']))
    JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={'message': 'Clear carts'})

@router.delete('/{row_id}')
def delete_item_cart(row_id, user: UserList = Depends(get_current_user)):
    delete_cart(user['_id'], row_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={'message': 'Delete item cart.'})
    