from fastapi import HTTPException
from api.server.database import db
from api.server.validation import validate_object_id
from api.models.product import ProductUpdatedSchema

async def create_product(name, description, price, image, code):
    product_dict = dict(
        name=name,
        description=description,
        price=price,
        image=image,
        code=code
    )
    
    product = await db.product_db.insert_one(product_dict)
    
    if product.inserted_id:
        product = await _get_product_or_404(product.inserted_id)
        return product

async def get_product(product_id):
    product = await _get_product_or_404(product_id)
    return product
    
async def get_all_products(skip=0, limit=50):
    products_cursor = db.product_db.find().skip(skip).limit(limit)
    products = await products_cursor.to_list(length=limit)
    return list(map(fix_product_id, products))

async def delete_product(product_id):
    await _get_product_or_404(product_id)
    product = await db.product_db.delete_one({'_id': validate_object_id(product_id) })
    if product.deleted_count:
        return {'status': f'deleted count: {product.deleted_count}'}


async def update_product(product_id, product_data: ProductUpdatedSchema):
    product = product_data.dict()
    product = {k: v for k, v in product.items() if v is not None}
    product_op = await db.product_db.update_one({'_id': validate_object_id(product_id)}, {'$set': product})
    
    if product_op.modified_count:
        return await _get_product_or_404(product_id)
    
    raise HTTPException(status_code=304)

async def _get_product_or_404(id):
    product = await db.product_db.find_one({'_id': validate_object_id(id)})
    if product:
        return fix_product_id(product)
    
    raise HTTPException(status_code=404, detail='Product not found')
    
def fix_product_id(product):
    if product.get("_id", False):
        product['_id'] =  str(product['_id'])
        return product
    else:
        raise ValueError(f'No `_id` found!: product - {product}')
    