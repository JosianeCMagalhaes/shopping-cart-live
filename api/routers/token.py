import jwt
from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from api.core import settings
from api.cruds.authentication import authentication_user

router = APIRouter(tags=['Token'], prefix='/token')

@router.post('')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authentication_user(form_data.username, form_data.password)
    if not user:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'data': 'User unauthorized'})

    user = {
        'id': str(user['_id']),
        'email': user['email'],
        'is_active': user['is_active'],
        'is_admin': user['is_admin']
    }

    token = jwt.encode(user, settings.JWT_SECRET,  algorithm="HS256")
    return JSONResponse(status_code=status.HTTP_200_OK, content={'access_token': token, 'token_type': 'bearer'})
