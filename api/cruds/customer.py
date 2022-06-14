from utils import Hash, _get_field_or_404, fix_id
from api.server.database import db
from api.models.customer import  CustomerSchema


async def create_customer(customer: CustomerSchema):
    password = Hash.encrypt(customer.password)
    customer['password'] = password
    customer = await db.customer_db.insert_one(customer.dict())
    
    if customer.inserted_id:
        customer = await _get_field_or_404(customer.inserted_id, db.customer_db, 'customer')
        return customer
    
async def get_customer(customer_id):
    customer = await _get_field_or_404(customer_id, db.customer_db, 'customer')
    return customer

async def get_all_customers(skip=0, limit=50):
    customer_cursor = db.customer_db.find().skip(skip).limit(limit)
    customers = await customer_cursor.to_list(length=limit)
    return list(map(fix_id, customers))

async def get_customer_by_email(email):
    return await db.customer_db.filter(email=email)

        