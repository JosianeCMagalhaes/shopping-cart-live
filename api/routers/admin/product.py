from fastapi import APIRouter, status, Depends
from starlette.responses import JSONResponse
from api.cruds.product import create_product, delete_product, update_product
from api.cruds.authentication import get_current_user_admin
from api.schemas.product import ProductList, ProductUpdatedSchema

router = APIRouter(tags=['Admin Product'], prefix='/admin/products')

@router.post('', response_model=ProductList, dependencies=[Depends(get_current_user_admin)])
async def create(product: ProductUpdatedSchema):
    result_product = await create_product(product)
    return JSONResponse(status_code=status.HTTP_200_OK, content=result_product)

@router.delete('/{product_id}', dependencies=[Depends(get_current_user_admin)])
async def delete(product_id):
    await delete_product(product_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content='')

@router.put('/{product_id}', response_model=ProductList, dependencies=[Depends(get_current_user_admin)])
async def update(product_id, product_request: ProductUpdatedSchema):
    product = await update_product(product_id, product_request)
    return JSONResponse(status_code=status.HTTP_200_OK, content=product)
