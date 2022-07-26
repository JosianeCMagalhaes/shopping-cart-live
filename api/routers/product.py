from typing import List
from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from api.schemas.product import ProductList
from api.cruds.product import get_product, get_all_products

router = APIRouter(tags=['Products'], prefix='/products')

@router.get('', response_model=List[ProductList])
async def products(skip=0, limit=100):
    products = await get_all_products(skip, limit)
    return JSONResponse(content={'data': {'products': products}}, status_code=status.HTTP_200_OK)

@router.get('/{product_id}', response_model=ProductList)
async def product(product_id):
    product = await get_product(product_id)
    return JSONResponse(content={'data': {'product': product}}, status_code=status.HTTP_200_OK)
