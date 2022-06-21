from fastapi import HTTPException, status
from api.server.database import db
from api.server.validation import validate_object_id
from api.schemas.product import ProductSchema, ProductUpdatedSchema

async def create_product(product: ProductSchema):
    try:
        product = await db.product_db.insert_one(product.dict())
        if product.inserted_id:
            product = await _get_product_or_404(product.inserted_id)
            return product
        return {}
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

async def get_product(product_id):
    product = await _get_product_or_404(product_id)
    return product

async def get_all_products(skip: int, limit: int):
    products_cursor = db.product_db.find().skip(int(skip)).limit(10)
    products = await products_cursor.to_list(length=int(limit))
    return list(map(fix_product_id, products))


async def delete_product(product_id):
    await _get_product_or_404(product_id)
    product = await db.product_db.delete_one({'_id': validate_object_id(product_id)})
    if product.deleted_count:
        return {'status': f'product deleted'}


async def update_product(product_id, product_data: ProductUpdatedSchema):
    product = product_data.dict()
    product = {k: v for k, v in product.items() if v is not None}
    product_op = await db.product_db.update_one({'_id': validate_object_id(product_id)}, {'$set': product})

    if product_op.modified_count:
        return await _get_product_or_404(product_id)

    raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)


async def _get_product_or_404(id):
    product = await db.product_db.find_one({'_id': validate_object_id(id)})
    if product:
        return fix_product_id(product)

    raise HTTPException(status_code=404, detail='Product not found')


def fix_product_id(product):
    if product.get("_id", False):
        product['_id'] = str(product['_id'])
        return product
    else:
        raise ValueError(f'No `_id` found!: product - {product}')
