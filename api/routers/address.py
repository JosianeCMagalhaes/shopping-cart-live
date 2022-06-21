from fastapi import APIRouter, Depends
from api.cruds.address import create_address_for_user, append_address_user, update_address
from api.cruds.authentication import get_current_user
from api.schemas.address import Address, AddressList, AddressSchema, AddressSchemaUpdate
from api.schemas.user import UserSchema
router = APIRouter(tags=['Address'], prefix='/adresses')

@router.post('', response_model=AddressList)
async def create_address(address: Address, user: UserSchema = Depends(get_current_user)):
    address = await create_address_for_user(user, address)
    return address

@router.post('/insert')
async def insert_address(address: Address, user: UserSchema = Depends(get_current_user)):
    address = await append_address_user(user['_id'], address)
    return address

@router.put('/{row_id}')
async def update_address_row(address_data: AddressSchemaUpdate, row_id, user: UserSchema = Depends(get_current_user)):
    address = await update_address(user['_id'], address_data, row_id)
    return address