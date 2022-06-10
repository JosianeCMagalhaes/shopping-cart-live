from fastapi import APIRouter, Depends, status
from cruds.product import create_product, get_product, get_products
from db.database import database
from schemas.product import ProductList
from typing import List

router = APIRouter(tags=['Admin Products'], prefix='/admin/products')

@router.post('/create', response_model=ProductList, dependencies=[Depends(database)])
def create(name, description, price, weight, code):
    return create_product(name, description, price, weight, code)

@router.get('/list', response_model=List(ProductList), dependencies=[Depends(database)])
def list(skip, limit):
    return get_products(skip, limit)

@router.get('/detail/{product_id}', response_model=ProductList, dependencies=[Depends(database)])
def product(product_id):
    return get_product(product_id)

