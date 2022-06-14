from fastapi import APIRouter, Depends
from api.models.product import ProductList
from api.cruds.product import get_product, get_all_products
from typing import List

router = APIRouter(tags=['Product'], prefix='/product')

@router.get('', response_model=List[ProductList])
async def products(skip, limit):
    return await get_all_products(skip, limit)


@router.get('/{product_id}', response_model=List[ProductList])
def product(product_id):
    return get_product(product_id)
