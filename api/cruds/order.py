from fastapi import status
from fastapi.responses import JSONResponse
from api.models.product import ProductSchema
from utils import _get_field_or_404, fix_id
from api.server.database import db
from api.models.order import OrderSchema
from api.models.customer import CustomerSchema, CustomerList
from api.cruds.cart import get_all_carts, delete_all_carts


async def get_order_by_customer(customer: CustomerSchema):
    orders = await db.order_db.filter(customer=customer)
    return list(map(fix_id, orders))


async def create_order(customer: CustomerList, address):
    price_total = 0
    carts = get_all_carts(customer._id)
    if len(carts) == 0:
        return {'error': 'carts are empty'}
    for cart in carts:
        price_total += float(cart['product_price'])

    order_data = dict(
        customer=customer,
        price=price_total,
        paid=False,
        address=address
    )

    order = await db.order_db.insert_one(order_data)

    if order.inserted_id:
        order = await _get_field_or_404(order.inserted_id, db.order_db, 'order')
        return order
    
    for cart in carts:
        order_item_data = dict(
            order=OrderSchema,
            product=ProductSchema
        )

        order_item = await db.order_item_db.insert_one(order_item_data)
        if order_item.inserted_id:
            order_item = await _get_field_or_404(order_item.inserted_id, db.order_item_db, 'order item')
            return order_item

        delete_all_carts(customer._id)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content= {'massage': 'create order.'})
        
        