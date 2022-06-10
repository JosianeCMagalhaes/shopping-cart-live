
from models.customer import Customer
from schemas.customer import CustomerCreate
from utils import Hash


def create_customer(customer: CustomerCreate):
    pwd_hash = hash.bcrypt(customer.password)
    db_customer = Customer(name=customer.name, email=customer.email, password=pwd_hash, is_active=True, is_adm=False)
    db_customer.save()
    return db_customer

def get_customer(customer_id):
    return Customer.filter(Customer.id == customer_id).first()

def get_customers(skip=0, limit=50):
    return list(Customer.select().offset(skip).limit(limit))

def get_customer_by_email(email):
    return Customer.filter(Customer.email == email).first()
    