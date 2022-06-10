from fastapi import APIRouter, Depends
from db.database import get_database
from schemas.product import ProductList
from cruds.product import get_products, get_product

router = APIRouter(tags=['Products'], prefix='/products')

async def products(skip, limit):
    return get_products(skip, limit)
