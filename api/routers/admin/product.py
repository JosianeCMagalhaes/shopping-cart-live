from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from api.models.product import ProductList, ProductUpdatedSchema
from api.cruds.product import get_product, get_all_products, create_product, delete_product, update_product
from typing import List

router = APIRouter(tags=['Admin Product'], prefix='/admin/product')

@router.post('', response_model=ProductList)
async def create(name, description, price, image, code):
    product = await create_product(name, description, price, image, code)
    return product

@router.get('', response_model=List[ProductList])
async def list(skip, limit):
    return await get_all_products(skip, limit)

@router.get('/{product_id}', response_model=List[ProductList])
async def product(product_id):
    return await get_product(product_id)

@router.delete('/{product_id}')
async def delete(product_id):
    await delete_product(product_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={'message': 'Product deleted.'})

@router.put('/{product_id}', response_model=List[ProductList])
async def update(product_id, product_request: ProductUpdatedSchema):
    product = await update_product(product_id, product_request)
    return product
