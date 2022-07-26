import logging
from ..utils import get_field_or_404
from fastapi import HTTPException, status
from api.server.database import db
from api.server.validation import validate_object_id
from api.schemas.address import Address, AddressSchemaUpdate

logger = logging.getLogger(__name__)

async def create_address_for_user(user, address):
    try:
        address_data = dict(
            user=user,
            address=[address])

        address = await db.address_db.insert_one(dict(address_data))
        if address.inserted_id:
            address = await get_field_or_404(address.inserted_id, db.address_db, 'address')
            return address
    except Exception as e:
        logger.exception(f'create_address_for_user.error: {e}')
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def append_address_user(user_id, address_data: Address):
    try:
        address = address_data.dict()
        address = {k: v for k, v in address.items() if v is not None}
        add_address = await db.address_db.find_one({'user._id': validate_object_id(user_id)})

        add_address['address'] = [{**v, 'is_delivery': False} for v in add_address['address']
                                  if v['is_delivery'] == address['is_delivery'] and address['is_delivery'] == True]
        add_address['address'].append(address)

        address_op = await db.address_db.update_one({'_id': validate_object_id(add_address['_id'])}, {'$set': add_address})
        if address_op.modified_count:
            return await get_field_or_404(add_address['_id'], db.address_db, 'address')

        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
    except Exception as e:
        logger.exception(f'append_address_user.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def update_address(user_id, address_data: AddressSchemaUpdate, row_id):
    try:
        address = address_data.dict()
        address = {k: v for k, v in address.items() if v is not None}
        address_op = await db.address_db.update_one({'user._id': validate_object_id(user_id)}, {'$set': {f'address.{row_id}': address}})

        if address_op.modified_count:
            return await get_field_or_404(address_op._id, db.address_db, 'address')

        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
    except Exception as e:
        logger.exception(f'update_address.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def get_address_by_user(user_id):
    try:
        address = await db.address_db.find_one({'user._id': validate_object_id(user_id)})
        if address:
            address['address'] = [ad for ad in address['address']
                                  if ad['is_delivery'] == True]
            return address
    except Exception as e :
        logger.exception(f'update_address.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
