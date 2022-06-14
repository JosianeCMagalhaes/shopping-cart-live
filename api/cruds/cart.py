import redis
import uuid

redis = redis.Redis(host='localhost', port=6379, db=1)

EXPIRED_CART = 900  # 15 minutos


def add_cart(**kwargs):
    customer_id, product_id, row_id = kwargs.values()

    for customer_carts in redis.scan_iter(f'carts:{customer_id}:*'):
        data = {index.decode('utf-8'): value.decode('utf-8')
                for index, value in redis.hgetall(customer_carts).items()}
        if int(data['customer_id']) == customer_id and int(data['product_id']) == product_id:
            return 'item already in cart'

    key = f'carts:{customer_id}:{uuid.uuid4().hex}'

    for index, value in kwargs.items():
        redis.hset(key, index, value)

    redis.expire(key, EXPIRED_CART)
    result = {key.decode('utf-8'): value.decode('utf-8')
              for key, value in redis.hgetall(key).items()}

    return result


def get_all_carts(customer_id):
    result = []
    for customer_carts in redis.scan_iter(f"carts:{customer_id}:*"):
        data = {index.decode('utf-8'): value.decode('utf-8')
                for index, value in redis.hgetall(customer_carts).items()}
        result.append(data)
    return result


def delete_cart(customer_id, row_id):
    return redis.delete(f"carts:{customer_id}:{row_id}")


def delete_all_carts(customer_id):
    for x in redis.scan_iter(f'carts:{customer_id}:*'):
        redis.delete(x)
    
