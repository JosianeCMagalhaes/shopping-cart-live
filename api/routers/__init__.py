from fastapi import APIRouter
from api.routers import account
from api.routers import address
from api.routers import cart
from api.routers import order
from api.routers import product
from api.routers import token
from api.routers.admin import product as product_adm
from api.routers.admin import user as user_adm

api_router = APIRouter()

api_router.include_router(account.router)
api_router.include_router(address.router)
api_router.include_router(cart.router)
api_router.include_router(order.router)
api_router.include_router(product.router)
api_router.include_router(token.router)
api_router.include_router(product_adm.router)
api_router.include_router(user_adm.router)