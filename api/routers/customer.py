from hashlib import new
import imp
from sqlite3 import DatabaseError
from timeit import default_timer
from venv import create
from fastapi import APIRouter
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks
from api import cruds
from api.cruds import customer
from db.database import get_database
from models.customer import Customer as CustomerDB
from schemas.customer import Customer
from cruds.customer import get_customer_by_email, create_customer

router = APIRouter(tags=['Accounts'], prefix='/accounts')


@router.post('/customer/', response_model=Customer, dependencies=[Depends(get_database)])
def register(customer: Customer):
    # verifica se o usuario do email já existe antes de criar
    if get_customer_by_email(customer.email):
        raise HTTPException(status_code=400, detail='Email já registrado')
    
    customer = create_customer(customer)
    return customer


