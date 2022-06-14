from fastapi import APIRouter
from api.routers import product
from api.routers.admin import product as product_adm

api_router = APIRouter()

api_router.include_router(product.router)
api_router.include_router(product_adm.router)