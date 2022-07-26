import logging
import jwt
import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..utils import Hash
from api.core import settings
from api.server.database import db
from api.server.validation import validate_object_id

logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def authentication_user(email, password):
    try:
        user = await db.user_db.find_one({'email': email})
        if not user['is_active']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User is not active')
        
        if not user:
            return False

        if not Hash.verify(password, user['password']):
            return False
        
        return user
    except Exception as e:
        logger.exception(f'authentication_user.error: {e}')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256']) 
        user = await db.user_db.find_one({'_id': validate_object_id(payload.get('id'))})
    except Exception as e:
        logger.exception(f'get_current_user.error: {e}')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid e-mail or password')

    return user 
    
async def get_current_user_admin(token: str = Depends(oauth2_scheme)):
    try:
        detail = 'Invalid e-mail or password'
        user = await get_current_user(token)
        if user['is_admin'] == False:
            detail = 'protected'
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
    except Exception:
        logger.exception(f'get_current_user_admin.error: {e}')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

    return user