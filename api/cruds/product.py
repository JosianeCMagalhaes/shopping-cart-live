from math import prod
import uuid
from fastapi import HTTPException, status
from models.product import Product
from schemas.product import ProductList


def create_product(name, description, price, weight, code):
    new_product = Product(
        name=name,
        description=description,
        price=price,
        weight=weight,
        code=code
    )

    new_product.save()
    return new_product

def get_product(product_id):
    product = Product.filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Produto não encontrado')
    return product

def get_products(skip=0, limit=50):
    return list(Product.select().offset(skip).limit(limit))


def delete_product(product_id):
    product = get_product(product_id)
    product.delete_instance()
    return 'Done'
