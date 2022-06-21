from ..utils import _get_field_or_404
from api.server.database import db
from api.schemas.order import OrderSchema
from api.schemas.product import ProductSchema
from api.schemas.user import UserSchema, UserList
from api.cruds.cart import get_all_carts, delete_all_carts
from api.cruds.address import get_address_by_user
from api.cruds.product import get_product

async def get_orders_by_user(user: UserSchema):
    orders = await db.order_db.find_one({'user._id': user['_id']})
    orders['_id'] = str(orders['_id'])
    orders['user']['_id'] = str(orders['user']['_id'])
    orders['address']['_id'] = str(orders['address']['_id'])
    return orders

async def create_order(user: UserList):
    price_total = 0
    carts = get_all_carts(user['_id'])
    
    if len(carts) == 0:
        return {'error': 'carts are empty'}
    
    for cart in carts:
        price_total += float(cart['product_price'])

    address = await get_address_by_user(user['_id'])
    
    order_data = dict(
        user=user,
        price=price_total,
        paid=False,
        address=address
    )

    order = await db.order_db.insert_one(order_data)
    if order.inserted_id:
        order = await _get_field_or_404(order.inserted_id, db.order_db, 'order')    
        
    for cart in carts:
        product = await get_product(cart['product_id'])
        order_item_data = dict(
            order=order,
            product=product
        )

        order_item = await db.order_item_db.insert_one(order_item_data)
        if order_item.inserted_id:
            order_item = await _get_field_or_404(order_item.inserted_id, db.order_item_db, 'order item')
            return order_item

        delete_all_carts(user['_id'])
        
        
        