import logging
from motor.motor_asyncio import AsyncIOMotorClient

class Database():
    client: AsyncIOMotorClient = None
    product_db = None
    gallery_db = None
    customer_db = None
    order_db = None
    order_item_db = None
    
    
db = Database()

async def connect_db():
    db.client = AsyncIOMotorClient(str("localhost:27017"), maxPoolSize=10, minPoolSize=10)
    db.product_db = db.client.shopping_cart.product
    db.gallery_db = db.client.shopping_cart.gallery
    db.customer_db = db.client.shopping_cart.customer
    db.order_db = db.client.shopping_cart.order
    db.order_item_db = db.client.shopping_cart.order_item
    
    logging.info('connect to database')
    
async def close_conn_db():
    db.client.close()