import logging
from fastapi import status, HTTPException
from ..utils import Hash, get_field_or_404,fix_id
from api.schemas.user import UserSchema, UserSchemaUpdate
from api.server.database import db
from api.server.validation import validate_object_id

logger = logging.getLogger(__name__)

async def create_user(user: UserSchema):
    try:
        password = Hash.encrypt(user.password)
        user.password = password
        user = await db.user_db.insert_one(user.dict())

        if user.inserted_id:
            user = await get_field_or_404(user.inserted_id, db.user_db, 'user')
            return user
    except Exception as e:
        logger.exception(f'create_user.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        
async def get_user(user_id):
    user = await get_field_or_404(user_id, db.user_db, 'user')
    return user

async def get_users(skip, limit):
    try:
        user_cursor = db.user_db.find().skip(int(skip)).limit(int(limit))
        users = await user_cursor.to_list(length=int(limit))
        return list(map(fix_id, users))
    except Exception as e:
        logger.exception(f'get_users.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


async def get_user_by_email(email):
    user = await db.user_db.find_one({'email': email})
    return user

async def update_user(user_id, user_data: UserSchemaUpdate):
    try:
        data = dict(user_data)
        data = {k: v for k, v in data.items() if v is not None}
        user = await db.user_db.update_one({'_id': validate_object_id(user_id)}, {'$set': data})

        if user.modified_count:
            return await get_field_or_404(str(user), db.user_db, 'user')
        
        return status.HTTP_304_NOT_MODIFIED
    except Exception as e:
        logger.exception(f'update_user.error: {e}')
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
    
async def delete_user(user_id):
    try:
        user = await db.user_db.delete_one({'_id': validate_object_id(user_id)})
        if user.deleted_count:
            return {'status': 'User deleted'}
    except Exception as e:
        logger.exception(f'delete_user.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        