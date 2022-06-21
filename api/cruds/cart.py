import logging
import redis
import uuid
from fastapi import HTTPException, status
from api.core import settings
from api.schemas.cart import CartItemsSchema
from api.schemas.user import UserSchema

logger = logging.getLogger(__name__)
redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)

def add_cart(cart: CartItemsSchema):
    try:
        for user_carts in redis.scan_iter(f'carts:{cart.user_id}:*'):
            data = {index.decode('utf-8'): value.decode('utf-8') for index, value in redis.hgetall(user_carts).items()}
            if str(data['user_id']) == cart.user_id and str(data['product_id']) == cart.product_id:
                return 'item already in cart'
        
        cart.row_id = uuid.uuid4().hex
        key = f'carts:{cart.user_id}:{cart.row_id}'

        for index, value in cart:
            redis.hset(key, index, value)

        redis.expire(key, settings.EXPIRED_CART)
        result = {key.decode('utf-8'): value.decode('utf-8')
                for key, value in redis.hgetall(key).items()}

        return result
    except Exception as e:
        logger.exception(f'add_cart.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        

def get_all_carts(user_id):
    try:
        result = []
        for user_carts in redis.scan_iter(f"carts:{user_id}:*"):
            data = {index.decode('utf-8'): value.decode('utf-8')
                    for index, value in redis.hgetall(user_carts).items()}
            result.append(data)
        return result
    except Exception as e:
        logger.exception(f'get_all_carts.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
def delete_cart(user_id, row_id):
    return redis.delete(f"carts:{user_id}:{row_id}")

def delete_all_carts(user_id):
    for x in redis.scan_iter(f'carts:{user_id}:*'):
        redis.delete(x)

def get_carts(user: UserSchema):
    total_price = 0
    items = get_all_carts(user['_id'])
    for item in items:
        total_price += float(item['product_price'])
    
    return {'total_price': total_price, 'items': items}
